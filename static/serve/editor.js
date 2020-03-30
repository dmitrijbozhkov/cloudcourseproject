$("#editor").summernote({
  placeholder: "Hello stand alone ui",
  tabsize: 2,
  height: 120,
  toolbar: [
    ["style", ["bold", "italic", "underline", "clear"]],
    ["font", ["strikethrough", "superscript", "subscript"]],
    ["fontsize", ["fontsize"]],
    ["color", ["color"]],
    ["para", ["ul", "ol", "paragraph"]],
    ["table", ["table"]],
    ["height", ["height"]],
    ["view", ["fullscreen", "help"]]
  ],
  callbacks: {
    onChange: function(contents, editable) {
      $("#editor_data").val(contents);
    }
  }
});
