# patch-configmap

This project contains scrips that patch a configmap based on certain parameters.
- patch_configmap.py takes configmap key, and configmap value and applys it based on label filter

---

## Run the script

```
usage: patch-configmap.py [-h] [--dryrun] [--namespace NAMESPACE] [--maxclusters MAXCLUSTERS] [--labelvalue LABELVALUE] [--configmapname CONFIGMAPNAME] [--configparameter CONFIGPARAMETER] [--configvalue CONFIGVALUE]

optional arguments:
  -h, --help            show this help message and exit
  --dryrun              Specify if you want to simulate running without actual execution.
  --namespace NAMESPACE
                        Specify namespace to run against. If not passed, change will be applied accross all namespaces.
  --maxcms MAXCMS
                        Maximum number of configmaps to change.
  --labelvalue LABELVALUE
                        Specify label based on which we are doing a filter
  --configmapname CONFIGMAPNAME
                        Specify configmap name. - NOT USED AT THE MOMENT
  --configparameter CONFIGPARAMETER
                        Specify parameter of configmap.
  --configvalue CONFIGVALUE
                        Specify value for parameter of configmap you have specified.
```
