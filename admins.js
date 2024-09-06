

const mongoose = require("mongoose");
main() 
 .then(()=>{console.log("connection successful");})
 .catch(err=>console.log(err));
 async function main(){
  await mongoose.connect("mongodb://127.0.0.1:27017/project");
 }

const adminSchema = new mongoose.Schema({
    username: {
      type: String,
      required: true,
      unique: true
    },
    email: {
      type: String,
      required: true,
      unique: true
    },
    password: {
      type: String,
      required: true
    }
  });
  const Admin = mongoose.model('Admin', adminSchema);
 Admin.insertMany([
    {username:"Sneha",email:"snehaagarwal1600@gmail.com",password:2351070},
    {username:"Kanishk",email:"kanishkraj600@gmail.com",password:2351078},
    {username:"Vishal",email:"vishalsah1590@gmail.com",password:2354031},
    {username:"Ruba",email:"rubamuntaha12@gmail.com",password:2354032},
    {username:"Debanjan",email:"debanjandasmsd@gmail.com",password:2351082},
    {username:"Ankit",email:"aky00190@gmail.com",password:2351119}
 ]).then((res)=>{console.log(res);})