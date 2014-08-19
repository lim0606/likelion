function timeTo(time){
 
	var times = new Date();
	var resultString;
 
	var millisec;
	millisec = (new Date(time)).getTime();
	times.setTime(millisec);
	var month = times.getUTCMonth() + 1;
	if(month < 10){
		month = "0"+ month;
	}
	var date = times.getUTCDate();
	if(date < 10){
		date = "0" + date;
	}
 
	resultString = 
	times.getYear()+1900 + "-" + month + "-" + date + " "
	+times.getUTCHours() + ":" + times.getMinutes() + ":" + times.getSeconds();
	return resultString;
}
 
function getArticleAfterArticle(article_id)
{
	var EndArticle = false;
 
	$.ajax({
		url: "/more",
		dataType: 'json',
		data: {
			last_article_id : article_id
		},
 
		success: function(data){
			if(data.count == 0){
				alert("No more article exists");
				//$("#morebtn").hide();
				EndArticle =true;
			}else{
				for (var article_idx in data.article_list)
				{
					article = data.article_list[article_idx]
					string = "<div class='well' id='article_"+ article.id 
					+"'><h1><a href='/article/detail/"+ article.id +"'>"
					+ article.title +"</a></h1><h3>"+ article.author +"</h3><h6>"
					+ timeTo(article.date_created)
					+"</h6><p> "
					+ article.content +" </p> </div>";
					$(string).insertAfter($(".well:last"))
				}
 
			}
		},
 
		error: function(status){
			string = "<div class='well' id='article_"+ data.id
			+"'><h1>Error occured..</h1></div>";
			$("#results").append(string);
		}
	});
	return true;
 
}
 
$(document).ready(function() {
	var number = 0;
	var string;
 
	$.ajax({
		url: "/rows",
		dataType: 'json',
		success: function(data){
			number = data.rows - 4;
		}
	});
	$('#load_more_button').bind('click', function() {
		var article_id = $(".well:last").attr("article_id");
		getArticleAfterArticle(article_id);
		return false;
	});
});