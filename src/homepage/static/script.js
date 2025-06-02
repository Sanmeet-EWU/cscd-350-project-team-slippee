htmx.onLoad(function(elt) {
    let fromDropdown = document.querySelector("select[name='from']");
    let toDropdown = document.querySelector("select[name='to']");
    let secondInputDiv = document.getElementById("file-input-2");
    let originalToOptions = Array.from(toDropdown.options).map(opt => opt.cloneNode(true));


  fromDropdown.addEventListener("change", function () {
      let selectedFrom = fromDropdown.value;
      toDropdown.innerHTML = ""; // Clear existing options

          originalToOptions.forEach(option => {
        if (option.value === selectedFrom && option.value !== "") return; // skip same value
        toDropdown.appendChild(option.cloneNode(true));
      });
    if (this.value === "Ares") {
      secondInputDiv.style.display = "block";
      secondInputDiv.required = true;
    } else {
      secondInputDiv.style.display = "none";
      secondInputDiv.required = false;
    }
  }); })


  // Optional: file name display logic
  // document.getElementById("file-input-1").addEventListener("change", function () {
  //   document.getElementById("fileName1").textContent = this.files.length
  //     ? `Selected: ${this.files[0].name}`
  //     : "No file selected";
  // });
  //
  // document.getElementById("file-input-2").addEventListener("change", function () {
  //   document.getElementById("fileName2").textContent = this.files.length
  //     ? `Selected: ${this.files[0].name}`
  //     : "No file selected";
  // });