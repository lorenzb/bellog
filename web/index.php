<html>
<head>
<link href="style.css" rel="stylesheet" type="text/css">
<title>BelLog Interpreter</title>
</head>
<body>
<script type="text/javascript">
var compositePolicy = "The administrator first checks if the project leaders-Ann and Fred-agree on the pub attribute\n\
pub(F) :- (pub(F)@ann -plus- pub(F)@fred)\n\n\
The policy of the project leader Piet grants access to his researchers to any project file:\n\
pol(S,F)@piet :- (researcher(S)@piet ^ prj_file(F)@piet)\n\n\
The policy of Ann is\n\
pol(ann,F)@ann :- prj_file(F)@ann\n\
pol(S1,F)@ann :- (pol(S2,F)@ann ^ give_access(S1,F)@S2)\n\
The first rule grants Ann access to any project file F, and the second rule states that any subject S2 with access to F may delegate this access to any subject S1 by issuing a give_access attribute.\n\n\
To define for which requests are the policies of Piet and Ann applicable, admin issues the following rules:\n\
perm_piet(S,F) :- (pol(S,F)@piet < contains(projects,F) > false)\n\
perm_ann(S,F) :- (pol(S,F)@ann < contains(project_ann,F) > false)\n\
The first rules states that Piet's and Ann's policy are used only for requests to files contained in the folder 'projects' and, respectively, 'project_ann'.\n\n\
Admin composes the policies of Piet and Ann using the agree operator:\n\
pol_leaders(S,F) :- (perm_piet(S,F) -plus- perm_ann(S,F))\n\n\
Since this composition may result in gaps or conflicts, admin issues the following policy:\n\
pol(S,F) :- ((pol_leaders(S,F) -top-> prj_leader(S)) -bot-> pub(F)@admin)\n\
If there is a conflict, then this policy grants access only to policy leaders. If there is no applicable policy, then access is granted only to public files and folders.\n\n\
Finally, the administrator issues the policy:\n\
pol(S,F) :- (contains(F,F) ^ pol(S,X))\n\
which recursively propagates grant decisions to subfolders\n\n\
The contains relation is recursively defined as follows:\n\
contains(F1,F2) :- subfolder(F1,F2)@fs\n\
contains(F1,F3) :- (contains(F1,F2) ^ contains(F2,F3))\n\
subfolder(projects,project_piet)@fs :- true\n\
subfolder(projects,project_ann)@fs :- true\n\
subfolder(project_piet,foo)@fs :- true\n\
subfolder(project_ann,bar)@fs :- true";
var compositeReq = "pol(carol,foo)";
var delegationPolicy = "has_access(U,F) :- (has_access(U,Y) ^ contains(Y,F)@fs)\n\
contains(F1,F2)@fs :- (contains(F1,F)@fs ^ contains(F,F2)@fs)\n\
contains(music,jazz)@fs :- true\n\
contains(music,pop)@fs :- true\n\
contains(jazz,miles)@fs :- true\n\
has_access(alice,music) :- true\n\
has_access(bob,pop) :-true";
var delegationReq = "has_access(alice,jazz)";
var rbacPolicy = "has_per(U,P) :- (ua(U,R) ^ pa(R,P))\n\
ua(alice,r1) :- true\n\
ua(bob,r2) :- true\n\
pa(r1,p1) :- true\n\
pa(r1,p2) :- true";
var rbacReq = "has_per(alice,p1)";
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
  echo '<input type="button" class="gray" name="loadComposite" value="Composite Policy" onClick="loadPolicy(compositePolicy, compositeReq);">';
  echo '<input type="button" class="gray" name="loadRBAC" value="RBAC Policy" onClick="loadPolicy(rbacPolicy, rbacReq);">';
  echo '<input type="button" class="gray" name="loadDelegation" value="File Policy" onClick="loadPolicy(delegationPolicy, delegationReq);">';
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
