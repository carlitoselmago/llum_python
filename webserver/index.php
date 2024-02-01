<!DOCTYPE html>
<html>
<head>
    <title>Data Display</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function(){
            // Function to update data every 5 seconds
            function updateData() {
                $.getJSON('data.json', function(data) {
                    $('#dataContainer').html(JSON.stringify(data, null, 4));
                });
            }

            // Update data on page load
            updateData();

            // Set interval to update data every 5 seconds
            setInterval(updateData, 5000);
        });
    </script>
</head>
<body>
    <h1>Data Received</h1>
    <pre id="dataContainer"></pre>
</body>
</html>
