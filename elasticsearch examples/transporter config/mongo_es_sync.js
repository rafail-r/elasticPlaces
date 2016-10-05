
// create a pipeline that reads documents from a file, transforms them, and writes them
Source({name:"localmongo", namespace:"elasticPlaces.places"})
.transform({filename: "transformer.js", namespace:"elasticPlaces.places"})
.save({name:"es", namespace:"elasticplaces.places"});
