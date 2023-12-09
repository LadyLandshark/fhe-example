# Thrift file describing basic operations for server and client

struct File {
  1: string path,
  2: binary data,
  3: binary ctx,
  4. binary pub_key,
  5: binary relin_key,
  6: binary rotate_key
}
  

service FHE_Fileserver {
  i32 initialize[
  i32 upload_file(1: File f),
  File download_file(1: string path),
  i32 add_file(1: string path, 2: binary data)
}
