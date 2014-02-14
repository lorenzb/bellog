<html>
<head>
<title>BelLog Interpreter</title>
</head>
<body>
<h1>BelLog Interpreter</h1>
<?php 
  echo '<table style="width:300px">';
  echo '<form action="index.php" method="post">';
#  echo '<ul>';
#  echo '<li><a href="">Example1</a></li>';
#  echo '<li><a href="">Example2</a></li>';
#  echo '<li><a href="">Example3</a></li>';
#  echo '</ul>';
  echo '<tr><td>';
  if ($_POST['policy']) {
    #$policy = $_POST["policy"];
    $policy = preg_replace('/\n+/', "\n", trim($_POST['policy']));
  }
  if ($_POST['query']) {
    $query = $_POST['query'];
  }
  echo 'Policy<br>';
  echo '<textarea name="policy" rows="10" cols="70">';
  if ($policy) {
    echo $policy;
  }
  echo '</textarea>';
  echo '<br>';
  echo 'Query: <input type="text" name="query" ';
  if ($query) {
    echo "value=$query>";
  } else {
    echo "value=''>";
  }
  echo '<input type="submit" value="Evaluate"><br>';
  if ($query && $policy) {
    $formattedPolicy = str_replace("\n", "<next>", $policy);
    $ret = shell_exec("python src/runWeb.py -i \"$formattedPolicy\" -q \"$query\" 2>&1");
    echo "Result: <b>$ret</b>";
    echo "<br>";
  }
  echo '</td><td>';
  echo '<input type="button" name="loadEx1" value="Load Example 1" onClick="this.form.policy.value=\'p(X,Y) :- (p(X,Z) ^ p(Z,Y))\np(X,Y) : - q(X,Y)\nq(a,b) :- true\nq(b,c) :- top \';"><br>';
  echo '<input type="button" name="loadEx2" value="Load Example 2" onClick="this.form.policy.value=\'pol(X,Y) :- (polLeaders(X,Y) -false-> owner(X))\npolLeaders(X,Y) :- polPiet(X,Y)\npolLeaders(X,Y) :- polAnn(X,Y)\npolPiet(carol,lab) :- true\npolAnn(dave,lab) :- true\nowner(eve) :- true\';"><br>';
  echo '</td></tr></table>';
  echo '</form>';
?> 
</body>
</html>
