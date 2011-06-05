	<div><h5> John Smith </h5> 
								<p> San Francisco, CA</p>
								<p> Engineer, Food</p>
								</div>
	$(document).ready(function(){
			$("#blah").fcbkcomplete({
				addontab         : true,
				onselect         : function(){
					$.getJSON("data/sample_search_results.txt",  function(matches){
							for(var result in matches){
								var def = {
									"profile_pic": "img/profile_128.gif"
								}
								var thisresult = matches[result];
								$.extend(thisresult, def);
								
								var templ = "<li> <img src='{{profile_pic}}' /> <div> <h5> {{name}} </h5>  <p>{{location}} </p> <p> {{matched_skills}}</p> </div> </li>"
								var html = Mustache.to_html(templ, thisresult);
								
								$("#searchResults")
									.children("#instructions")
										.hide("")
										.end()
									.append(html).fadeIn();
							}
						
					})
				}
			});
		})