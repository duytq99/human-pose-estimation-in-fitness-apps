# human-pose-estimation-in-fitness-apps
## 1. Cài đặt môi trường và thư viện cần thiết
Project này được cài đặt trên môi trưởng ảo được tạo bởi `miniconda`. Lựa chọn phiên bản phù hợp và cài đặt `miniconda` tại [link](https://docs.conda.io/en/latest/miniconda.html).

Khởi tạo môi trường ảo sử dụng `miniconda` với phiên bản python là 3.7:
> `conda create --name <ml-project> python==3.7`

Các thư viện sử dụng trong project này được liệt kê ở file [requirements.txt](#requirements.txt), bao gồm:
- `tensorflow=1.14`: xây dựng mô hình mạng nơ-ron
- `numpy==1.21.2`: xử lý dữ liệu dạng ma trận số
- `pandas==1.1.5`: xử lý dữ liệu dạng bảng
- `scikit_learn==1.0.1`: xây dựng các mô hình học máy cơ bản
- `mediapipe`: Thư viện hỗ trợ trích xuất keypoints, sử dụng kiến trúc blazepose

Để cài đặt các thư viện trên, thực hiện lệnh sau:
>`pip install -r requirements.txt`

## 2. Cách thực hiện demo
Tải repo này và truy cập vào thư mục chính:
> `git clone https://github.com/duytq99/human-pose-estimation-in-fitness-apps.git`

> `cd human-pose-estimation-in-fitness-apps`

> `conda activate <env-name>`
> `python main.py --path <path-to-video> --draw`
> <path-to-video>: là đường dẫn đến video demo 
