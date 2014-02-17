<html>
<head>
<link href="style.css" rel="stylesheet" type="text/css">
<title>BelLog Interpreter</title>
</head>
<body>
<script type="text/javascript">
var example1 = "p(X,Y) :- (p(X,Z) ^ p(Z,Y))\n\
p(X,Y) :- q(X,Y)\n\
q(a,b) :- true\n\
q(b,c) :- top";
var example2 = "pol(X,Y) :- (polLeaders(X,Y) -top-> owner(X))\n\
polLeaders(X,Y) :- (polPiet(X,Y) -plus- polAnn(X,Y))\n\
polPiet(carol,lab) :- true\n\
polAnn(carol,lab) :- false\n\
polAnn(dave,lab) :- true\n\
owner(carol) :- true";
function loadPolicy(pol) {
  document.getElementById("policy").value = pol;
  document.getElementById("query").value = '';
}
</script>
<?php 
  echo '<table style="width:300px" id="table">';
  echo '<form action="index.php" method="post">';
  echo '<tr><td>';
  echo '<h1>BelLog Policy Interpreter</h1></td></tr><tr><td>';
  if ($_POST['policy']) {
    $policy = $_POST["policy"];
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
  echo '<input type="button" class="gray" name="loadEx1" value="Load Example 1" onClick="loadPolicy(example1);">';
  echo '<input type="button" class="gray" name="loadEx2" value="Load Example 2" onClick="loadPolicy(example2);">';
  echo '<br></td></tr><tr><td>';
  echo '<p>The request </p><input id="query" type="text" name="query" placeholder="Type a request" ';
  if ($query) {
    echo "value=$query>";
  } else {
    echo "value=''>";
  }
  echo '<input type="submit" class="gray" value="evaluates">';
  echo '<p> to : </p>';
  if ($query && $policy) {
    $policyFormatted = preg_replace('/\n+/', "<newline>", trim($policy));
    $ret = shell_exec("python src/runWeb.py -i \"$policyFormatted\" -q \"$query\" 2>&1");
    $length = strlen('Error');
    if (substr($ret, 0, $length) === 'Error') {
      echo "<br><br><p style='color:red'>$ret</p>";
    } else {
      echo "<p id='result'>$ret</p><br><br>";
    }
  }
  echo '</td></tr><tr><td>';
  echo '<br><br><p>For details on BelLog\'s syntax see: <a href="http://github.com/ptsankov/bellog/">http://github.com/ptsankov/bellog/</a></p>';
  echo '</td></tr></table>';
  echo '</form>';
?>
</body>
</html>
