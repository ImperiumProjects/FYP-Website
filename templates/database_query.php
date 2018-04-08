<?php 

echo "Test output";

$servername = "84.200.193.29";
$username = "scraper";
$password = "scraper";
$dbname = "historical";
$port = "3306";

$sql = "SELECT percentage FROM predictions ORDER BY id DESC LIMIT 1";

$con = mysqli_connect($servername, $username, $password, $dbname, $port) or die ("Could not connect");

$r = mysqli_query($con,$sql) or die ("No query");

$result = array();

while($row = mysqli_fetch_array($r)){
    array_push($result,array(
        'percentage'=>$row['percentage']
    ));
}

echo json_encode(array('result'=>$result));

mysqli_close($con);