<?php
	include 'dbconfig.php';
	
	$conn = mysqli_connect($host, $username, $password, $database);
	$playerusername = mysqli_real_escape_string($conn, $_GET['username']);
	$playerpassword = mysqli_real_escape_string($conn, $_GET['password']);

	if (mysqli_connect_errno()) 
	{
		exit('Failed to connect to MySQL: ' . mysqli_connect_error());
	}
	else 
	{
		if( isset($_GET['username']) )
		{
			$query = "SELECT Password, IsBanned FROM Accounts WHERE Username='$playerusername'";
			$queryresult = mysqli_query($conn, $query);
			
			if(mysqli_num_rows($queryresult) >= 1)
			{
				$querydata = mysqli_fetch_row($queryresult);
				if($playerpassword == $querydata[0])
				{
					if($querydata[1] == 1)
					{
						echo 0x02; # Banned
					}
					else
					{
						echo 0x01; # Success
					}
				}
				else
				{
					echo 0x06; # Incorrect Password
				}
			}
			else
			{
				echo 0x06; #Incorrect Username
			}
		}
		else
		{
			mysqli_close($conn);
			echo 0xff;
		}
	}

?>