const uploadBtn = document.getElementById('file_upload')
const fileName = document.getElementById('file_name')

console.log(uploadBtn.name)
uploadBtn.addEventListener('change', function() {
  fileName.textContent = this.files[0].name
})
