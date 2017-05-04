Poi = require('../models/attraction');

newPoi = new Poi({

    name: "test",
    types: ["bay", "urban"], 
    cityName: "Atlantis",
    cityPath: "/0",
    introduction: ["A mysterious place in Altantis", "To be explored..."],
    contact: ["Unknown"],
    // phone: String,
    // website: String,
    location: "The lost realm",
    ticket: "Unvaluable",
    openTime: "Till the end of world"
});

newPoi.save(function(err){
	if(err){
		console.log(err);
	}
});