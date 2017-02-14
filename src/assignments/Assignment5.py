from src.controller.QueryParser import QueryParser


queryParser = QueryParser();
query = raw_input('Enter your query:');
post_fix_tokens = queryParser.generate_postfix_expr(queryParser.stemQueryString(query));
result = queryParser.execute_postfix_tokens(post_fix_tokens);
print "List of containing documents is listed as below\n";
print sorted(result);