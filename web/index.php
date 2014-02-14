<html>
<head>
<title>BelLog Interpreter</title>
</head>
<body>
<h1>BelLog Interpreter</h1>
<form action="index.php" method="post">
<textarea name="policy" rows="10" cols="70">
p(X) :- q(X)
q(a) :- true
</textarea>
<br>
Query: <input type="text" name="query"> <input type="submit" value="Run">
</form>
<?php 
  if ($_POST["query"] && $_POST["policy"]) {
    $query = $_POST["query"];
    $policy = str_replace("\n", "<next>", $_POST["policy"]);
    $ret = shell_exec("python src/runWeb.py -i \"$policy\" -q \"$query\"");
    echo "Result: $ret";
    echo "<br>";
  }
?> 
</body>
</html>
