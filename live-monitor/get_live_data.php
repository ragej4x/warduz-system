<?php
$ph_file = "ph_log.txt";
$temp_file = "temperature_log.txt";

function get_last_line($file) {
    $lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    return end($lines);
}

$last_ph = get_last_line($ph_file);
$last_temp = get_last_line($temp_file);

$response = [
    "ph" => $last_ph ? explode(", ", $last_ph)[1] : "No data",
    "temperature" => $last_temp ? explode(", ", $last_temp)[1] . " °C, " . explode(", ", $last_temp)[2] . " °F" : "No data",
];

header('Content-Type: application/json');
echo json_encode($response);
?>
