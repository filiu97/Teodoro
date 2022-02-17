// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.


// Create a new database.
use Knowledge_Base

// Create a new collection.
db.general.insertMany([
{
    title : 'days',
    names : ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'],
    numbers : ['1', '2', '3', '4', '5', '6', '7']
},
{
  title : 'months',
  names : ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
  numbers : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
}
]
);
