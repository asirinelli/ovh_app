<html>
<head>
<title>Domain list</title>
</head>
<body>
<ul>
%for d in domains:
  <li><a href={{url}}/{{d}}>{{d}}</a></li>
%end
</ul>
</body>
</html>
