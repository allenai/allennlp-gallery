/**
 * This is a template that's compiled down to a definition of the
 * infrastructural resources required for running your application.
 *
 * For more information on the JSONNET language, see:
 * https://jsonnet.org/learning/getting_started.html
 */

// This file is generated once at template creation time and unlikely to change
// from that point forward.
local config = import '../skiff.json';
local util = import './util.libsonnet';

function(
    appImage, proxyImage, cause, sha, env='staging', branch='', repo='',
    buildId=''
)
    // A list of hostnames served by your application. By default your application's
    // `prod` environment will receive requests made to `$appName.apps.allenai.org` and
    // non-production environments will receive requests made to `$appName-$env.apps.allenai.org`.
    //
    // If you'd like to use a custom domain make sure DNS is pointed to the cluster's IP
    // address and add the domain to the `customDomains` list in `../skiff.json`.
    local hosts = util.getHosts(env, config);

    // In production we run two versions of your application, as to ensure that
    // if one instance goes down or is busy, end users can still use the application.
    // In all other environments we run a single instance to save money.
    local replicas = if env == 'prod' then 2 else 1;

    // Each app gets it's own namespace.
    local namespaceName = config.appName;

    // Since we deploy resources for different environments in the same namespace,
    // we need to give things a fully qualified name that includes the environment
    // as to avoid unintentional collission / redefinition.
    local fullyQualifiedName = config.appName + '-' + env;

    // Every resource is tagged with the same set of labels. These labels serve the
    // following purposes:
    //  - They make it easier to query the resources, i.e.
    //      kubectl get pod -l app=my-app,env=staging
    //  - The service definition uses them to find the pods it directs traffic to.
    local namespaceLabels = {
        app: config.appName,
        contact: config.contact,
        team: config.team
    };

    local labels = namespaceLabels + {
        env: env
    };

    // By default multiple instances of your application could get scheduled
    // to the same node. This means if that node goes down your application
    // does too. We use the label below to avoid that.
    local antiAffinityLabels = {
        onlyOneOfPerNode: config.appName + '-' + env
    };
    local podLabels = labels + antiAffinityLabels;

    // Annotations carry additional information about your deployment that
    // we use for auditing, debugging and administrative purposes
    local annotations = {
        "apps.allenai.org/sha": sha,
        "apps.allenai.org/branch": branch,
        "apps.allenai.org/repo": repo,
        "apps.allenai.org/build": buildId
    };

    // The port the NGINX proxy is bound to.
    local proxyPort = 8080;

    // The port the API (Python Flask application) is bound to.
    local appPort = 8000;

    // This is used to verify that the proxy (and thereby the UI portion of the
    // application) is healthy. If this fails the application won't receive traffic,
    // and may be restarted.
    local proxyHealthCheck = {
        port: proxyPort,
        scheme: 'HTTP'
    };

    // This is used to verify that the API is funtional.
    local appHealthCheck = {
        port: appPort,
        scheme: 'HTTP'
    };

    local namespace = {
        apiVersion: 'v1',
        kind: 'Namespace',
        metadata: {
            name: namespaceName,
            labels: namespaceLabels
        }
    };

    local tls = util.getTLSConfig(fullyQualifiedName, hosts);
    local ingress = {
        apiVersion: 'extensions/v1beta1',
        kind: 'Ingress',
        metadata: {
            name: fullyQualifiedName,
            namespace: namespaceName,
            labels: labels,
            annotations: annotations + tls.ingressAnnotations + {
                'kubernetes.io/ingress.class': 'nginx',
                'nginx.ingress.kubernetes.io/ssl-redirect': 'true'
            }
        },
        spec: {
            tls: [ tls.spec + { hosts: hosts } ],
            rules: [
                {
                    host: host,
                    http: {
                        paths: [
                            {
                                backend: {
                                    serviceName: fullyQualifiedName,
                                    servicePort: proxyPort
                                }
                            }
                        ]
                    }
                } for host in hosts
            ]
        }
    };

    local deployment = {
        apiVersion: 'apps/v1',
        kind: 'Deployment',
        metadata: {
            labels: labels,
            name: fullyQualifiedName,
            namespace: namespaceName,
            annotations: annotations + {
                'kubernetes.io/change-cause': cause
            }
        },
        spec: {
            revisionHistoryLimit: 3,
            replicas: replicas,
            selector: {
                matchLabels: labels
            },
            template: {
                metadata: {
                    name: fullyQualifiedName,
                    namespace: namespaceName,
                    labels: podLabels,
                    annotations: annotations
                },
                spec: {
                    # This block tells the cluster that we'd like to make sure
                    # each instance of your application is on a different node. This
                    # way if a node goes down, your application doesn't:
                    # See: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#node-isolation-restriction
                    affinity: {
                        podAntiAffinity: {
                            requiredDuringSchedulingIgnoredDuringExecution: [
                                {
                                   labelSelector: {
                                        matchExpressions: [
                                            {
                                                    key: labelName,
                                                    operator: "In",
                                                    values: [ antiAffinityLabels[labelName], ],
                                            } for labelName in std.objectFields(antiAffinityLabels)
                                       ],
                                    },
                                    topologyKey: "kubernetes.io/hostname"
                                },
                            ]
                        },
                    },
                    containers: [
                        {
                            name: fullyQualifiedName + '-app',
                            image: appImage,
                            args: [ 'start.py', '--prod' ],
                            # The "probes" below allow Kubernetes to determine
                            # if your application is working properly.
                            #
                            # The readiness probe is used to determine if
                            # an instance of your application can accept live
                            # requests. The configuration below tells Kubernetes
                            # to stop sending live requests to your application
                            # if it returns 3 non 2XX responses over 30 seconds.
                            # When this happens the application instance will
                            # be taken out of rotation and given time to "catch-up".
                            # Once it returns a single 2XX, Kubernetes will put
                            # it back in rotation.
                            #
                            # The liveness probe is used to determine if an
                            # instance needs to be restarted. The configuration
                            # below tells Kubernetes to restart the application
                            # if it's unhealthy for 90 seconds. You can increase
                            # the `failureThreshold` if your API is slow.
                            #
                            # The route that's used by these probes should not
                            # depend on any external services, it should purely
                            # assess the health of your local application.
                            #
                            # Lastly, the `initialDelaySeconds` instructs
                            # Kubernetes to wait 30 seconds before starting the
                            # liveness probe. This is to give your application
                            # time to start. If your application needs more time
                            # you should increase this value and give things
                            # a little headroom, things are always a little slower
                            # in the cloud :).
                            #
                            # Kubernetes also has a livenessProbe that can be used to restart
                            # deadlocked processes. You can find out more about it here:
                            # https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-command
                            #
                            # We don't use a livenessProbe as it's easy to cause unnecessary
                            # restarts, which can be really disruptive to a site's availability.
                            # If you think your application is likely to be unstable after running
                            # for long periods send a note to reviz@allenai.org so we can work
                            # with you to craft the right livenessProbe.
                            readinessProbe: {
                                httpGet: appHealthCheck + {
                                    path: '/?check=readiness_probe'
                                },
                                periodSeconds: 10,
                                failureThreshold: 3
                            },
                            # This tells Kubernetes what CPU and memory resources your API needs.
                            # We set these values low by default, as most applications receive
                            # bursts of activity and accordingly don't need dedicated resources
                            # at all times.
                            #
                            # Your application will be allowed to use more resources than what's
                            # specified below. That said your application might be killed if it
                            # uses more than what's requested. If you know you need more memory
                            # or that your workload is CPU intensive, consider increasing the
                            # values below.
                            #
                            # Currently all pods (the collection of containers defined here)
                            # cannot request more than 23.9 GB of RAM or 3.92 (3920m) CPU
                            # cycles. If you need more resources reach out to reviz@allenai.org,
                            # we can provide accomodations on a case by case basis.
                            #
                            # If your application is of high criticality and you'd like to ensure
                            # maximum availability, reach out to reviz@allenai.org for help modifying
                            # these settings.
                            #
                            # See the following for more information on these values:
                            # https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#how-pods-with-resource-requests-are-scheduled
                            resources: {
                                requests: {
                                    cpu: '50m',
                                    memory: '500Mi'
                                }
                            },
                        },
                        {
                            name: fullyQualifiedName + '-proxy',
                            image: proxyImage,
                            readinessProbe: {
                                httpGet: proxyHealthCheck + {
                                    path: '/proxy_health?check=rdy'
                                }
                            },
                            resources: {
                                requests: {
                                   cpu: '50m',
                                   memory: '100Mi'
                                }
                            }
                        }
                    ]
                }
            }
        }
    };

    local service = {
        apiVersion: 'v1',
        kind: 'Service',
        metadata: {
            name: fullyQualifiedName,
            namespace: namespaceName,
            labels: labels,
            annotations: annotations
        },
        spec: {
            selector: labels,
            ports: [
                {
                    port: proxyPort,
                    name: 'http'
                }
            ]
        }
    };

    [
        namespace,
        ingress,
        deployment,
        service
    ]
