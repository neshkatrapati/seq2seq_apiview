<html>
<head>
  <link rel="stylesheet" href="/static/bootstrap/dist/css/bootstrap.css"></link>
</head>
<body>
  <div class="container">
    <div class="col-md-12">
      <div class="row">
        <h1>All Models</h1>
      </div>

      <div class="row">
          <form method="post" action="/">
          <div class="col-md-12">
              <div class="row" style="margin-bottom: 2%">

                    <div class="col-md-4">
                      <select name="model_list" id='model_list' class="form-control" style="width: auto">
                      % for model_name, model_details in models.items():
                          % if model_name == selected_model :
                            <option value="{{ model_name }}" selected>{{ model_details['description'] }}</option>
                          % else:
                            <option value="{{ model_name }}">{{ model_details['description'] }}</option>
                          % end
                      % end
                      </select>
                    </div>
              </div>
              <div class="row" style="margin-bottom: 2%">
                    <div class="col-md-12">
                        <div class="row">
                        <div class="col-md-12">
                            <div>
                                <label for="join_output">Join Output ?</label>
                                <input type="checkbox" id="join_output" name="join_output" {{ join_output }}>
                                <button type="button" class="btn btn-sm btn-danger" onclick="clearInput();">Clear Input</button>
                            </div>
                            <textarea name="input_text" style="width: auto" id="input_text">{{ input_text }}</textarea>
                        </div>
                        </div>
                        <div class="row" style="margin-top: 2%">
                        <div class="col-md-12">
                            <div id="output_text" style="width: auto" class="card">
                                <div class="card-body">
                                {{ output_text }}
                                </div>
                            </div>
                        </div>
                        </div>
                        <div class="row" style="margin-top: 2%">

                        <div class="col-md-12">
                            <div> Try this with a json call at <a href="/i/{{ selected_model }}/json">/i/{{ selected_model }}/json</a> </div>
                            <div id="json_text" style="width: auto" class="card">
                                <div class="card-body">
                                curl -H "Content-Type: application/json" -X POST -d '{{ json_text }}' {{ source_url }}Ti/{{ selected_model }}/json
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>
              </div>
              <div class="row" style="margin-bottom: 2%">
                  <div class="col-md-12">
                    <input type="submit" value="Submit" class="btn btn-primary" />
                  </div>
              </div>
          </div>
        </form>
        </div>
      </div>
    </div>
  <script type="text/javascript">
      clearInput = function() {
          document.getElementById('input_text').innerText = "";
          document.getElementById('join_output').checked = false;
      }
  </script>
  </div>

</body>

</html>
