<?php
function timediference($givenTimeString){


    // Convert the given time string to a DateTime object
    // Assuming the date is today, first get today's date in Y-m-d format
    $todayDate = date('Y-m-d');
    // Combine the date and time into a single string
    $dateTimeString = $todayDate . ' ' . str_replace('_', ':', $givenTimeString);
    // Create a DateTime object for the given time
    $givenDateTime = date_create($dateTimeString);

    // Create a DateTime object for the current time
    $currentDateTime = date_create('now');

    // Calculate the difference as a DateInterval object
    $difference = date_diff($currentDateTime, $givenDateTime);

    // Convert the difference to total minutes (including fractions for seconds)
    $differenceInMinutes = ($difference->h * 60) + $difference->i + ($difference->s / 60);

    // If the difference is negative, adjust the value to reflect the past time
    if ($currentDateTime < $givenDateTime) {
        $differenceInMinutes = -$differenceInMinutes;
    }

    // Output the difference in minutes as a float
    return $differenceInMinutes;
}
?>