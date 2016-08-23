library(jsonlite)

## Full docs available here: http://docs.ckan.org/en/latest/api/index.html#module-ckan.logic.action.get

reqstr <- "http://energydata.uct.ac.za/api/3/action/"
allResources <- "current_package_list_with_resources"
groupList <- "group_list"
projectList <- "organization_list"

yourstr <- readline("Please type the request you want to send to the data portal (allResources)")

data <- fromJSON(paste(reqstr, yourstr))
names(data$result)

packageList <- fromJSON(paste(reqstr, "datastore_search?resource_id=_table_metadata", sep = ""))

fromJSON(paste(reqstr, "package_list", sep = ""))
fromJSON("http://energydata.uct.ac.za/api/3/action/package_search?q=ind")
fromJSON("http://energydata.uct.ac.za/api/3/action/package_search?q=version:1.0")

##User Management
#get.user_list
fromJSON("http://energydata.uct.ac.za/api/3/action/user_list")$result

#get.package_show resources associated with a specific dataset
fromJSON("http://energydata.uct.ac.za/api/3/action/package_show?id=residential")$result["resources"]

fromJSON("http://energydata.uct.ac.za/api/3/action/member_list?id=transport&Authorization=c391d0f4-e31e-4aac-a359-03ab746a12a3")
("http://energydata.uct.ac.za/api/3/action/organization_member_create?id=uct-energy-research-centre&username=bruno&role=editor&api-key=c391d0f4-e31e-4aac-a359-03ab746a12a3")