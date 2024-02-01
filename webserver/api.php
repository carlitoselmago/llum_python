<?php
$dbFile = 'llum.db';
$db = new SQLite3($dbFile);

// Check if the required GET parameters are present
if (isset($_GET['sensor']) && isset($_GET['lastupdate']) && isset($_GET['battery'])) {
    $sensorId = (int)$_GET['sensor'];
    $lastUpdate = SQLite3::escapeString($_GET['lastupdate']);
    $battery=(float)$_GET['battery'];
    // Prepare the update query
    $query = "UPDATE sensors SET lastupdate = '$lastUpdate', battery='$battery'  WHERE id = $sensorId";

    // Execute the update
    if ($db->exec($query)) {
        echo "Sensor data updated successfully.";
    } else {
        echo "Error updating sensor data.";
    }
} else {
    echo "Missing required parameters.";
}
?>
