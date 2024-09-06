const mongoose = require("mongoose");
main() 
 .then(()=>{console.log("connection successful");})
 .catch(err=>console.log(err));
 async function main(){
  await mongoose.connect("mongodb://127.0.0.1:27017/project");
 }


const facedetectedSchema = new mongoose.Schema({
  numberOfMales: {
    type: Number,
    required: true
  },
  numberOfFemales: {
    type: Number,
    required: true
  },
  numberOfFemaleAlone: {
    type: Number
  },
  numberOfFemaleSurroundedByMale: {
    type: Number
  }
});

const facedetected = mongoose.model("facedetected", facedetectedSchema);