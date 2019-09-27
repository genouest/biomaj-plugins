# BioMAJ plugins

This repo contains plugins for BioMAJ.

Plugins define a *release*, *name* and *list* method.

* release fetch the latest release
* name returns the plugin name (used in bank property files)
* list returns the list of files to download
* [optional] download fetches files to offline directory

An example bank property file is provided along plugin.

Plugin directory must be specified in global.properties or *bank*.properties file.
