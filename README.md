# ASCII ART

将图片转换为 ASCII ART，在终端中打印结果，并将 ASCII ART 保存为图片。

## 功能

- 读取常见图片格式，例如 JPG、PNG、BMP。
- 将图片转换为灰度 ASCII 字符画。
- 在终端直接打印 ASCII ART。
- 将 ASCII ART 渲染并保存为图片文件。
- 支持自定义输出宽度、字体大小和亮度反转。

## 安装依赖

```powershell
python -m pip install -r requirements.txt
```

## 使用方法

在 `ASCII_ART` 目录下运行：

```powershell
python image_to_ascii.py path\to\input.jpg
```

指定输出图片路径：

```powershell
python image_to_ascii.py path\to\input.jpg -o output.png
```

调整 ASCII ART 宽度：

```powershell
python image_to_ascii.py path\to\input.jpg --width 160
```

如果终端背景较暗，可以尝试反转亮度映射：

```powershell
python image_to_ascii.py path\to\input.jpg --invert
```

调整保存图片时使用的字体大小：

```powershell
python image_to_ascii.py path\to\input.jpg --font-size 14
```

## 参数说明

- `image`：输入图片路径。
- `-o, --output`：输出图片路径，默认 `ascii_art.png`。
- `-w, --width`：终端 ASCII ART 宽度，默认 `120`。
- `--invert`：反转字符亮度映射。
- `--font-size`：保存图片时使用的字体大小，默认 `12`。

## 示例

```powershell
python image_to_ascii.py sample.jpg -o sample_ascii.png --width 120
```

运行后，脚本会先在终端打印 ASCII ART，然后保存图片到 `sample_ascii.png`。
