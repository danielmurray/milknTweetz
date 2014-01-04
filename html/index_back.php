<html>
<head><title>dandz</title>
</head>
<body>
<?php
$con=mysqli_connect("127.0.0.1","ai_user","letmein","milkntweetz");

// Check connection
if (mysqli_connect_errno())
{
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
echo "our splended results</br>";
$result = mysqli_query($con,"SELECT * from temp");
while($row = mysqli_fetch_array($result))
  {
  echo $row['name'] . " " . $row['value'];
  echo "<br>";
  }

      mysqli_close($con);
?>
</body>
</html>

