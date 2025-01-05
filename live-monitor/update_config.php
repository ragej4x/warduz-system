<?php
if (isset($_POST['mode']) && isset($_POST['red']) && isset($_POST['green']) && isset($_POST['blue'])) {
    $mode = $_POST['mode'];
    $red = $_POST['red'];
    $green = $_POST['green'];
    $blue = $_POST['blue'];

    $configContent = "mode=$mode\n";
    $configContent .= "red=$red\n";
    $configContent .= "green=$green\n";
    $configContent .= "blue=$blue\n";

    $configFile = 'config.txt';
    if (file_put_contents($configFile, $configContent)) {
        echo json_encode(['status' => 'success', 'message' => 'Config updated successfully.']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Failed to update config file.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Missing required data.']);
}
?>
