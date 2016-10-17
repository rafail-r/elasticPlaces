module.exports = function(doc) {
  var new_data = {};
  new_data["_id"] = doc["data"]["_id"]["$oid"];
  new_data["geometry"] = doc["data"]["geometry"];
  new_data["name"] = doc["data"]["name"];
  new_data["formatted_address"] = doc["data"]["formatted_address"];
  new_data["rating"] = doc["data"]["rating"];
  new_data["types"] = doc["data"]["types"];
  doc["data"] = new_data
  //console.log("transformer: " + JSON.stringify(doc));
  return doc
}



