module.exports = function(doc) {
  var new_data = {};
  new_data["_id"] = doc["data"]["_id"]["$oid"];
  new_data["firstName"] = doc["data"]["firstName"];
  doc["data"] = new_data;
  //console.log("transformer: " + JSON.stringify(doc));
  return doc
}



