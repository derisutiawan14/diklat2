// Function Invocation
// function myFunction(a, b) {
//   return a * b;
// }
// console.log(myFunction(10, 2));

// Function Invocation object global
// let x = myFunction();  
// function myFunction() {
//   return this;
// }

// Function Invocation metode object 
// const myObject = {
//     firstName: "John",
//     lastName: "Doe",
//     fullName: function() {
//         return this.firstName + " " + this.lastName;
//     }
// }
// console.log(myObject.fullName());

// const myObject2 = {
//   firstName: "John",
//   lastName: "Doe",
//   fullName: function() {
//     return this;
//   }
// }
// console.log(myObject2.fullName());

// // Function Invocation Function Construtor
// function myFunction(arg1, arg2) {
//     this.firstName = arg1;
//     this.lastName = arg2;
// }

// // // Buat instance baru dari myFunction
// const person1 = new myFunction("John", "Doe");
// const person2 = new myFunction("Mary", "Smith");
// console.log(person1);
// console.log(person2);

// // Function Call
// const person = {
//   fullName: function(city, country) {
//     return this.firstName + " " + this.lastName + ", " + city + ", " + country;
//   }
// };

// const person1 = {
//   firstName: "John",
//   lastName: "Doe"
// };
// console.log(person.fullName.call(person1, "Oslo", "Norway")); 

// // Function Apply
// console.log(person.fullName.apply(person1, ["Oslo", "Norway"]));

// Function Bind
// const person2 = {
//   firstName: "John",
//   lastName: "Doe",
//   fullName: function() {
//     return this.firstName + " " + this.lastName;
//   }
// };

// const member = {
//   firstName: "Hege",
//   lastName: "Nilsen"
// };

// let fullName = person2.fullName.bind(member);
// console.log(fullName()); // Mengembalikan "Hege Nilsen"

// Function Closures
function makeCounter() {
    let count = 0;
    return function() {
      count++;
      return count;
    };
  }
  
  let counter = makeCounter();
  console.log(counter()); 
  console.log(counter());