<!doctype html>
<html>
    <head>
        <title>{{ page_title }}</title>
        <link rel="stylesheet" href="static/main.css"/>
    </head>
    <body>

        <h4>WIND MESSAGES LIST </h4>
        <h4></h4>
        <h5>.................................................................. </h5>
       <table border = 0 WIDTH="30%" HEIGHT="5%"CELLPADDING="0" CELLSPACING="0">
         {% for i in range(n): %}
            <tr>
               <td> <small>{{ height_atc[i]}}</small></td>
                <td>........ </td>
               <td><small>{{ sender_atc[i]}}</small></td>
                <td>.......... </td>
               <td align=right><small>{{atc[i]}}</small></td>

            </tr>

         {% endfor %}
       </table>


    </body>

</html>



