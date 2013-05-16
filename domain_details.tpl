<html>
<head>
<title>Details for {{domain}}</title>
</head>
<body>
<table border="0">
%for d in subdomains:
  <tr>
  <td>{{d['subDomain']}}</td>
  <td>{{d['fieldType']}}</td>
  <td>{{d['target']}}</td>
  </tr>
%end
</table>
</ul>
</body>
</html>
