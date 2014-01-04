<!DOCTYPE html>
<html lang="en">
    <head>
   
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />

    <title>Dandzy</title>
    
    
    <meta name="description" content="">
    <meta name="author" content="">

    <link href="/css/bootstrap.css" rel="stylesheet">
    <link href="/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="/css/datepicker.css" rel="stylesheet">
    
    <link rel="stylesheet" href="/css/nanoscroller.css">
    <link rel="stylesheet" href="/css/reveal.css">
    <link href="/css/style.css" rel="stylesheet">
    <!--<link rel="shortcut icon" class="icon-random">-->
    <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />
    
        <!-- Le HTML5 shim, for ddIE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    
    <script src="/js/jquery-1.7.1.min.js"></script>
    <script src="/js/jquery.reveal.js" type="text/javascript"></script>
    <script src="/js/bootstrap.js"></script>
    <script src="/js/bootstrap-dropdown.js"></script>
    <script src="/js/bootstrap-datepicker.js"></script>
  </head>

  <body>
    <div id="main_container" class="container">
        <div class="wrapper">
        <div class="navbar">
    <div id="navbar_fill" class="fill">
        <div id="navbar_container" class="container">
            <a class="brand" href="/">Dandzy</a>
            <ul class="nav">
            </ul>
            <ul class="nav nav-pills pull-right">

                <span style="display: inline-block;">
                    <form class="form-search" style="margin-bottom: 0px;" action="javascript:void(0)" onSubmit="search_global(this)">
                      <span class="input-prepend">
                        <button type="submit" class="btn" style="margin-top:2px;"><i class="icon-search"></i></button>
                        <input name="s_content" id="s_content" type="text" class="span2 search-query color-light-striped" style="margin-top:2px;">
                      </span>
                    </form>
                </span>
                <span class="social" style="display:float-left;">
                    
                    <a title="GitHub" href="#" class="zgithub"><img src="/images/cat.png" onmouseover="this.src='/images/cat_active.png'" onmouseout="this.src='/images/cat.png'"></a>
                    <a title="Twitter" href="#" class="ztwitter"><img src="/images/bird.png" onmouseover="this.src='/images/bird_active.png'" onmouseout="this.src='/images/bird.png'"></a>
                    <a title="RSS" href="#" class="zrss"><img src="/images/rss.png" onmouseover="this.src='/images/rss_active.png'" onmouseout="this.src='/images/rss.png'"></a>
                </span>
                
            </ul>
        </div>
    </div>
</div><div class="topbar">
      <div id="topbar_fill" class="fill">
        <div id="topbar_container" class="container">
            
            <!--<ul class="nav nav-pills pull-right">
                <li class="dropdown" id="myname">
                  
                   <li><a href="#">Sign in</a></li><br/>                
            </ul>-->
        </div>
      </div>
   </div>    
        <div class="container-fluid">
              <div class="row-fluid">
                <div class="span12">
        <div id="contentForm" class="row span10 offset1">
    <div class="span4 nano" style="margin-left:5px; margin-right: 10px; height:470px;">
	</br><h4>Under Construction: <small>AI class project</small></h4>
   </div>

    <div class="span8" style="margin-left: 0px;height:500px;">
	</br>
    <!--here we go-->
    <?php
	$con=mysqli_connect("127.0.0.1","ai_user","letmein","milkntweetz");

	// Check connection
	if (mysqli_connect_errno())
	{
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
	echo "<h4>our splended results</h4>";
	$result = mysqli_query($con,"SELECT * from objects");
	while($row = mysqli_fetch_array($result))
	{
	  if($row['asin'] != null) {//http://www.amazon.com/gp/product/B00C7ATZMK
	  	echo "<a href='https://www.amazon.com/gp/product/".$row['asin']."'>".$row['name'] . "</a> -- " . $row['description'];
	  } else {
	  	echo $row['name'] . " -- " . $row['description'];
	  }
	  echo "<br>";
	}

	      mysqli_close($con);
	?>

	    </div><!--/.fluid-container-->
    </div></div></div></div>
    <div class="footer">

	    <p><strong>&copy; Dandzy 2013</strong> an artificial alternative to consumer driven product review.
		<br/>
	    </p>
   </div>    

  </body>
</html>


