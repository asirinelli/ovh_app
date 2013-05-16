<html>
<head>
<title>Send SMS</title>
</head>
<body>
<form action="{{url}}" method="post">
Sender: <select name="sender">
%for sender in senders:
  <option value="{{sender['sender']}}">{{sender['description']}} ({{sender['sender']}})</option>
%end
</select>
<br>
Recipient: <input type="text" name="recipient"><br>
Text: <textarea name="text" rows="20" cols="30"></textarea><br>
<input type="submit" value="Send">
</form>
</body>
</html>
