import os
import sys
from os.path import join
from pathlib import Path

import coloredlogs
import argparse
import logging
from kubernetes import client, config

DOCKER_KUBE_FILE = "/app/.kube/config"
LOCAL_KUBE_FILE = join(Path.home(), ".kube/config")

def load_kube_config(ctx=None):
    if os.path.isfile(DOCKER_KUBE_FILE):
        logger.info("running in container, detected config")
        config.load_kube_config(config_file=DOCKER_KUBE_FILE, context=ctx)
    elif os.path.isfile(LOCAL_KUBE_FILE):
        logger.info("running locally, detected config")
        config.load_kube_config(config_file=LOCAL_KUBE_FILE, context=ctx)
    else:
        config.load_incluster_config()


def patch_cm(target_namespace,target_cm,target_label,cm_parameter,cm_value,dry_run, max_cm_to_patch):

    if cm_parameter == None or cm_value == None:
        logger.error(
            f"No configmap parameter or value set. We will exit here."
        )
        sys.exit()
    
    nmb_cr_patched = 0

    labelSelector = f"configtype={target_label}"
    
    logger.info("Changing all configmaps with a label")

    if target_label == None:
        logger.error(
            f"No label value parameter set. We will exit here."
        )
        sys.exit()

    if target_namespace is None:
        namespaces_list = client.CoreV1Api().list_namespace()
    else:
        field_selector = f"metadata.name={target_namespace}"
        namespaces_list = client.CoreV1Api().list_namespace(field_selector=field_selector)

    for namespace in namespaces_list.items:
        resp = client.CoreV1Api().list_namespaced_config_map(namespace.metadata.name, label_selector=labelSelector)
        if len(resp.items) != 0:
            logger.info(f"Changing value of {cm_parameter} for configmap name {resp.items[0].metadata.name}, from namespace: {namespace.metadata.name}")
            
            if cm_parameter not in resp.items[0].data:
                logger.info(f"Key {cm_parameter} does not exists in a ConfigMap, adding it now...")

            resp.items[0].data[cm_parameter] = cm_value
            patch_configmap(resp.items[0], dry_run)

            if nmb_cr_patched >= max_cm_to_patch:
                logger.warning(
                    f"Reached the max number of postgresCluster to patch ({max_cm_to_patch}). Stopping here"
                )
                break


def patch_configmap(configmap, dry_run):
    if dry_run:
        logger.warning(f"As DRYRUN is active, we will not make any actual changes.")
    else:
        client.CoreV1Api().patch_namespaced_config_map(
            name=configmap.metadata.name,
            namespace=configmap.metadata.namespace,
            body=configmap,
        )
        logger.debug(f"cluster {configmap.metadata.name} patched")


def main():
    logger.info(f"Start patching CR config ...")

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--dryrun", action='store_true', help="Specify if you want to simulate running without actual execution.") 
    argParser.add_argument("--namespace", help="Specify namespace to run against. If not passed, change will be applied accross all namespaces.")
    argParser.add_argument("--maxcms", help="Maximum number of configmaps to change.", default=20, type=int)
    argParser.add_argument("--labelvalue", help="Specify label based on which we are doing a filter.")
    argParser.add_argument("--configmapname", help="Specify configmap name.")
    argParser.add_argument("--configparameter", help="Specify parameter of configmap.")
    argParser.add_argument("--configvalue", help="Specify value for parameter of configmap you have specified.")

    args = argParser.parse_args()

    logger.info(
        f"max number of cluster to patch is set to {args.maxclusters}. Change this value using MAX_PGCLUSTER_TO_PATCH parameter"
    )

    if args.dryrun:
        logger.warning("DRY_RUN is set to TRUE. No modification will be performed!")

    patch_cm(
        args.namespace,
        args.configmapname,
        args.labelvalue,
        args.configparameter,
        args.configvalue,
        args.dryrun,
        args.maxcms);

    logger.info("Patching completed!")


if __name__ == "__main__":
    # use coloredlogs instead of std log
    global logger
    logger = logging.getLogger(__name__)
    coloredlogs.install(
        level="INFO", fmt="%(asctime)s [%(levelname)s] %(programname)s: %(message)s"
    )

    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        sys.exit()
    logger.info(f"Starting ConfigMap patching for contest {active_context['name']}...")

    load_kube_config()
    main()