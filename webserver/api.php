<?php
// api.php

// Check if there are GET parameters
if (!empty($_GET)) {
    // Define the path to the JSON file
    $jsonFilePath = 'data.json';

    // Read the existing data from the file
    $data = file_exists($jsonFilePath) ? json_decode(file_get_contents($jsonFilePath), true) : [];

    // Merge new data with existing data
    $data = array_merge($data, $_GET);

    // Save the merged data back to the file
    file_put_contents($jsonFilePath, json_encode($data));
}

echo "Data received and stored.";
?>
