<html>
<head>
<link href="style.css" rel="stylesheet" type="text/css">
<title>BelLog Interpreter</title>
</head>
<body>

<?php 
  echo '<table style="width:300px" id="table">';
  echo '<form action="index.php" method="post">';
#  echo '<ul>';
#  echo '<li><a href="">Example1</a></li>';
#  echo '<li><a href="">Example2</a></li>';
#  echo '<li><a href="">Example3</a></li>';
#  echo '</ul>';
  echo '<tr><td>';
  echo '<h1>BelLog Policy Interpreter</h1></td></tr><tr><td>';
  if ($_POST['policy']) {
    #$policy = $_POST["policy"];
    $policy = preg_replace('/\n+/', "\n", trim($_POST['policy']));
  }
  if ($_POST['query']) {
    $query = $_POST['query'];
  }
  echo '<textarea id="policy" name="policy" rows="10" cols="70" placeholder="Enter a policy or load one of the examples located on the left">';
  if ($policy) {
    echo $policy;
  }
  echo '</textarea>';
  echo '</td><td valign="top">';
  echo '<input type="submit" class="gray" name="loadEx1" value="Load Example 1" onClick="this.form.policy.value=\'p(X,Y) :- (p(X,Z) ^ p(Z,Y))\np(X,Y) : - q(X,Y)\nq(a,b) :- true\nq(b,c) :- top \';"><br>';
  echo '<input type="submit" class="gray" name="loadEx2" value="Load Example 2" onClick="this.form.policy.value=\'pol(X,Y) :- (polLeaders(X,Y) -false-> owner(X))\npolLeaders(X,Y) :- polPiet(X,Y)\npolLeaders(X,Y) :- polAnn(X,Y)\npolPiet(carol,lab) :- true\npolAnn(dave,lab) :- true\nowner(eve) :- true\';"><br>';
  echo '</td></tr><tr><td>';
  echo '<input id="query" type="text" name="query" placeholder="Type a request" ';
  if ($query) {
    echo "value=$query>";
  } else {
    echo "value=''>";
  }
  echo '<input type="submit" class="gray" value="Evaluate">';
  if ($query && $policy) {
    $formattedPolicy = str_replace("\n", "<next>", $policy);
    $ret = shell_exec("python src/runWeb.py -i \"$formattedPolicy\" -q \"$query\" 2>&1");
    echo "<p id='result'>$ret</p>";
  }
  echo '</td></tr><tr><td>';
  echo '<br><br><br><br><p>For details on BelLog\'s syntax see: <a href="http://github.com/ptsankov/bellog/">http://github.com/ptsankov/bellog/</a></p>';
  echo '</td></tr></table>';
  echo '</form>';
?> 
</body>
</html>
