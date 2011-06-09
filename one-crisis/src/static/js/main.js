	$(document).ready(function(){
			var x = function(){
				var qs = []
				$(".bit-box").each(function(a,item){
				    qs.push($(item).text());
				});
				var finalQs = "skills=" + qs.join("&skills=") + "&location=" + $("#location").val();
				
				$.post("search", finalQs, function(matches){
					matches = $.parseJSON(matches);
					for(var result in matches){
						var def = {
							"profile_pic": "img/profile_128.gif"
						}
						var thisresult = matches[result];
						$.extend(thisresult, def);
						
						var templ = "<li id='profile_{{id}}'> <img src='{{profile_pic}}' /> <div> <h5> {{name}} </h5>  <p>{{location}} </p> <p> {{matched_skills}}</p> </div> </li>"
						var html = Mustache.to_html(templ, thisresult);
						
						$("#searchResults")
							.children("#instructions")
								.hide("")
								.end()
							.append(html).fadeIn();
					}
				
			})
				
			}
			$("#btnSearch").click(x)
		
			$("#searchResults")
				.delegate("li", "click", function(){
					var id= this.id.replace("profile_", "");
					window.location = window.location + "profile?id=" + id;
				});
			
			$("#blah").fcbkcomplete({
				addontab         : true
				/*onselect         : function(){
					x()
					
					//$.getJSON("data/sample_search_results.txt",  function(matches){
						
				}*/
			});
		})