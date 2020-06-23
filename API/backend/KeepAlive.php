<?php
	include 'dbconfig.php';
	
	$conn = mysqli_connect($host, $username, $password, $database);
	$InstanceID = mysqli_real_escape_string($_GET['InstanceID']);
	
	if (mysqli_connect_errno()) 
	{
		exit('Failed to connect to MySQL: ' . mysqli_connect_error());
	}
	else 
	{
		$query = "SELECT * FROM WorldInstances WHERE InstanceID='$InstanceID'";
		$queryresult = mysqli_query($conn, $query);
			
		if (mysqli_num_rows($queryresult) > 0)
		{
			$current_time = time()
			$command = "UPDATE WorldInstances SET LastUpdate='$current_time' WHERE InstanceID='$InstanceID'";
			
			if (mysqli_query($conn, $command) === TRUE)
			{
				return 0x01
			}
			else
			{
				return 0xfe
			}
		}
		else
		{
			return 0xff
		}
	}
?>