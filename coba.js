const jsonStr = '{"nama":"John Doe","umur":30,"kota":"Jakarta","hobi":["membaca","bermain musik","olahraga"]}';

const obj = JSON.parse(jsonStr);
console.log(obj.nama); // Output: John Doe
console.log(obj.umur); // Output: 30
console.log(obj.hobi[0]); // Output: membaca