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
var req1 = "p(a,c)";
var req2 = "pol(carol,lab)";
function loadPolicy(pol, req) {
  document.getElementById("policy").value = pol;
  document.getElementById("query").value = req;
  document.getElementById("output").innerHTML= "";
}
</script>
<?php 
  echo '<table style="width:300px" id="table">';
  echo '<form action="index.php" method="post">';
  echo '<tr class="title"><td>';
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
  echo '<input type="button" class="gray" name="loadEx1" value="Example 1" onClick="loadPolicy(example1, req1);">';
  echo '<input type="button" class="gray" name="loadEx2" value="Example 2" onClick="loadPolicy(example2, req2);">';
  echo '<br></td></tr><tr class="request"><td>';
  echo '<br><br><p class="reqtext">Request</p></td></tr>';
  echo '<tr><td><br><input id="query" type="text" name="query" placeholder="Type a request" ';
  if ($query) {
    echo "value=$query>";
  } else {
    echo "value=''>";
  }
  echo '<input type="submit" class="gray" value="evaluate"></td></tr><tr><td><br></td></tr>';
  if ($query && $policy) {
    $policyFormatted = preg_replace('/\n+/', "<newline>", trim($policy));
    $ret = shell_exec("python src/runWeb.py -i \"$policyFormatted\" -q \"$query\" 2>&1");
    $length = strlen('Error');
    if (substr($ret, 0, $length) === 'Error') {
      echo "<tr class='error' id='output'><td>$ret</td></tr>";
    } else {
      echo "<tr class='result' id='output'><td>$ret</td></tr>";
    }
  }
  echo '<tr><td>';
  echo '<br><br><br><br><br><hr/><p>For details on BelLog\'s syntax see: <a href="http://github.com/ptsankov/bellog/">http://github.com/ptsankov/bellog/</a></p>';
  echo '</td></tr></table>';
  echo '</form>';
?>
</body>
</html>
