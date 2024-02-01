<?php
$dbFile = 'llum.db';
$db = new SQLite3($dbFile);

$timedout=18; //minutes
$batteryalert=0.2;

include_once("_helpers.php");
echo '<link  href="styles.css" rel="stylesheet" type="text/css">';

// Prepare the select query to fetch all sensor data
$query = "SELECT id, battery, lastupdate FROM sensors ORDER BY id ASC";

// Execute the query
$results = $db->query($query);

// Check if there are any results
if ($results) {
    echo "<h2>Sensor Data:</h2>";
    echo "<table border='1'><tr><th>ID</th><th>Battery</th><th>Last Update</th></tr>";

    // Loop through the results and display them
    while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
        echo "<tr>";
        echo "<td>" . htmlspecialchars($row['id']) . "</td>";
        $class="";
        if ($row['battery']<$batteryalert){
            $class="recharge";
        }
        echo "<td><span class='".$class."'> " . htmlspecialchars($row['battery']) . "%</span></td>";
        $timediff=round(timediference($row['lastupdate']),2);
        $class="";
        if ($timediff>$timedout){
            $class="timedout";
        }
        echo "<td><span class='".$class."'> " . htmlspecialchars($timediff) . " min</span></td>";
        echo "</tr>";
    }

    echo "</table>";
} else {
    echo "No sensor data available.";
}
?>



<?php
/*


// Specify the path to the JSON file
$jsonFilePath = 'data.json';

// Read the JSON file
$jsonData = file_get_contents($jsonFilePath);

// Decode the JSON data into a PHP array
$data = json_decode($jsonData, true);

// Check if data was successfully decoded
if ($data) {
    // Display the 'secondsleft' value
    echo "Seconds Left: " . $data['secondsleft'] . "<br>";

    // Check if 'sensors' array is available and not empty
    if (!empty($data['sensors'])) {
        echo "<h2>Sensors:</h2>";
        // Iterate through the 'sensors' array
        foreach ($data['sensors'] as $index => $sensor) {
            echo "<div class='sensor'>Sensor " . ($index) . ": ";
            echo "Battery: " . $sensor['battery'] . " ";
            echo "Last Update: " . $sensor['lastupdate'] . " ";
            echo '</div>';
        }
    } else {
        echo "No sensor data available.";
    }
} else {
    echo "Error decoding JSON data.";
}
*/
?>
