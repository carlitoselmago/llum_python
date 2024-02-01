<?php
$dbFile = 'llum.db';
$db = new SQLite3($dbFile);

// Create table query
$query = "CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY,
    battery REAL,
    lastupdate TEXT
);";
$db->exec($query);

$db->exec('BEGIN;');
for($x=0;$x<12;$x++){
    $query="INSERT INTO sensors (id,battery,lastupdate) VALUES (".$x.",0.0,'00_00_00')";
    if (!$db->exec($query)) {
        echo "Error inserting row $x\n";
    }
}
$db->exec('COMMIT');
// Execute the query to create the table


echo "Database and table created successfully.";
?>
