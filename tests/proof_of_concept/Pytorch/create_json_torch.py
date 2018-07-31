from copy import deepcopy
import json

# This code has been created with the pytorch documentation from "https://pytorch.org/docs/stable/nn.html"
# Random samples parameter not included in FractionalMaxPool2D as the documentation does not specify the type

# The final dictionary to be dumped to JSON
layers_dict = dict()

# The different strings present in the dictionaries are declared below
optional = "optional"
_type = "type"
path = "path"
_int = "int"
_tuple = "tuple"
_bool = "bool"
_float = "float"
default = "default"
params = "params"

# The different layers defined are declared below
conv1d = "CONV1D"
conv2d = "CONV2D"
conv3d = "CONV3D"
transpose1d = "CONVTRANSPOSE1D"
transpose2d = "CONVTRANSPOSE2D"
transpose3d = "CONVTRANSPOSE3D"
unfold = "UNFOLD"
fold = "FOLD"

maxpool1d = "MAXPOOL1D"
maxpool2d = "MAXPOOL2D"
maxpool3d = "MAXPOOL3D"
maxunpool1d = "MAXUNPOOL1D"
maxunpool2d = "MAXUNPOOL2D"
maxunpool3d = "MAXUNPOOL3D"
avgpool1d = "AVGPOOL1D"
avgpool2d = "AVGPOOL2D"
avgpool3d = "AVGPOOL3D"
fractionalmaxpool2d = "FRACTIONALMAXPOOL2D"
lppool1d = "LPPOOL1D"
lppool2d = "LPPOOL2D"
adaptivemaxpool1d = "ADAPTIVEMAXPOOL1D"
adaptivemaxpool2d = "ADAPTIVEMAXPOOL2D"
adaptivemaxpool3d = "ADAPTIVEMAXPOOL3D"
adaptiveavgpool1d = "ADAPTIVEAVGPOOL1D"
adaptiveavgpool2d = "ADAPTIVEAVGPOOL2D"
adaptiveavgpool3d = "ADAPTIVEAVGPOOL3D"

reflectionpad1d = "REFLECTIONPAD1D"
reflectionpad2d = "REFLECTIONPAD2D"
replicationpad1d = "REPLICATIONPAD1D"
replicationpad2d = "REPLICATIONPAD2D"
replicationpad3d = "REPLICATIONPAD3D"
zeropad2d = "ZEROPAD2D"
constantpad1d = "CONSTANTPAD1D"
constantpad2d = "CONSTANTPAD2D"
constantpad3d = "CONSTANTPAD3D"

elu = "ELU"
hardshrink = "HARDSHRINK"
hardtanh = "HARDTANH"
leakyrelu = "LEAKYRELU"
logsigmoid = "LOGSIGMOID"
prelu = "PRELU"
relu = "RELU"
relu6 = "RELU6"
rrelu = "RRELU"
selu = "SELU"
sigmoid = "SIGMOID"
softplus = "SOFTPLUS"
softshrink = "SOFTSHRINK"
softsign = "SOFTSIGN"
tanh = "TANH"
tanhshrink = "TANKHSHRINK"
threshold = "THRESHOLD"
softmin = "SOFTMIN"
softmax = "SOFTMAX"
softmax2d = "SOFTMAX2D"
logsoftmax = "LOGSOFTMAX"

# The different parameters for the layers are declared below
in_channels = "in_channels"
out_channels = "out_channels"
kernel_size = "kernel_size"
stride = "stride"
padding = "padding"
dilation = "dilation"
groups = "groups"
bias = "bias"
return_indices = "return_indices"
output_size = "output_size"
output_ratio = "output_ratio"
ceil_mode = "ceil_mode"
count_include = "count_include"
norm_type = "norm_type"
value = "value"
alpha = "alpha"
inplace = "inplace"
lambd = "lambd"
min_val = "min_val"
max_val = "max_val"
min_value = "min_value"
max_value = "max_value"


# Convolution 1D Layer Definition
in_channels_dict = dict()
in_channels_dict[_type] = [_int]
in_channels_dict[optional] = False

out_channels_dict = dict()
out_channels_dict[_type] = [_int]
out_channels_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

groups_dict = dict()
groups_dict[_type] = [_int]
groups_dict[optional] = True
groups_dict[default] = 1

bias_dict = dict()
bias_dict[_type] = _bool
bias_dict[optional] = True
bias_dict[default] = True

conv_params = dict()
conv_params[in_channels] = deepcopy(in_channels_dict)
conv_params[out_channels] = deepcopy(out_channels_dict)
conv_params[kernel_size] = deepcopy(kernel_size_dict)
conv_params[stride] = deepcopy(stride_dict)
conv_params[padding] = deepcopy(padding_dict)
conv_params[dilation] = deepcopy(dilation_dict)
conv_params[groups] = deepcopy(groups_dict)
conv_params[bias] = deepcopy(bias_dict)

conv_dict = dict()
conv_dict[path] = "torch.nn.Conv1d"
conv_dict[params] = deepcopy(conv_params)

layers_dict[conv1d] = deepcopy(conv_dict)

# Convolution 2D Layer Definition
in_channels_dict = dict()
in_channels_dict[_type] = [_int]
in_channels_dict[optional] = False

out_channels_dict = dict()
out_channels_dict[_type] = [_int]
out_channels_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

groups_dict = dict()
groups_dict[_type] = [_int]
groups_dict[optional] = True
groups_dict[default] = 1

bias_dict = dict()
bias_dict[_type] = _bool
bias_dict[optional] = True
bias_dict[default] = True

conv_params = dict()
conv_params[in_channels] = deepcopy(in_channels_dict)
conv_params[out_channels] = deepcopy(out_channels_dict)
conv_params[kernel_size] = deepcopy(kernel_size_dict)
conv_params[stride] = deepcopy(stride_dict)
conv_params[padding] = deepcopy(padding_dict)
conv_params[dilation] = deepcopy(dilation_dict)
conv_params[groups] = deepcopy(groups_dict)
conv_params[bias] = deepcopy(bias_dict)

conv_dict = dict()
conv_dict[path] = "torch.nn.Conv2d"
conv_dict[params] = deepcopy(conv_params)

layers_dict[conv2d] = deepcopy(conv_dict)

# Convolution 3D Layer Definition
in_channels_dict = dict()
in_channels_dict[_type] = [_int]
in_channels_dict[optional] = False

out_channels_dict = dict()
out_channels_dict[_type] = [_int]
out_channels_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

groups_dict = dict()
groups_dict[_type] = [_int]
groups_dict[optional] = True
groups_dict[default] = 1

bias_dict = dict()
bias_dict[_type] = _bool
bias_dict[optional] = True
bias_dict[default] = True

conv_params = dict()
conv_params[in_channels] = deepcopy(in_channels_dict)
conv_params[out_channels] = deepcopy(out_channels_dict)
conv_params[kernel_size] = deepcopy(kernel_size_dict)
conv_params[stride] = deepcopy(stride_dict)
conv_params[padding] = deepcopy(padding_dict)
conv_params[dilation] = deepcopy(dilation_dict)
conv_params[groups] = deepcopy(groups_dict)
conv_params[bias] = deepcopy(bias_dict)

conv_dict = dict()
conv_dict[path] = "torch.nn.Conv3d"
conv_dict[params] = deepcopy(conv_params)

layers_dict[conv3d] = deepcopy(conv_dict)

# Transposed 1D Convolution Layer
in_channels_dict = dict()
in_channels_dict[_type] = [_int]
in_channels_dict[optional] = False

out_channels_dict = dict()
out_channels_dict[_type] = [_int]
out_channels_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

output_padding_dict = dict()
output_padding_dict[_type] = [_int, _tuple]
output_padding_dict[optional] = True
output_padding_dict[default] = 0

groups_dict = dict()
groups_dict[_type] = [_int]
groups_dict[optional] = True
groups_dict[default] = 1

bias_dict = dict()
bias_dict[_type] = _bool
bias_dict[optional] = True
bias_dict[default] = True

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1


transpose_params = dict()
transpose_params[in_channels] = deepcopy(in_channels_dict)
transpose_params[out_channels] = deepcopy(out_channels_dict)
transpose_params[kernel_size] = deepcopy(kernel_size_dict)
transpose_params[stride] = deepcopy(stride_dict)
transpose_params[padding] = deepcopy(padding_dict)
transpose_params[dilation] = deepcopy(dilation_dict)
transpose_params[groups] = deepcopy(groups_dict)
transpose_params[bias] = deepcopy(bias_dict)

transpose_dict = dict()
transpose_dict[path] = "torch.nn.ConvTranspose1d"
transpose_dict[params] = deepcopy(transpose_params)

layers_dict[transpose1d] = deepcopy(transpose_dict)

# Transposed 2D Convolution Layer
in_channels_dict = dict()
in_channels_dict[_type] = [_int]
in_channels_dict[optional] = False

out_channels_dict = dict()
out_channels_dict[_type] = [_int]
out_channels_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

output_padding_dict = dict()
output_padding_dict[_type] = [_int, _tuple]
output_padding_dict[optional] = True
output_padding_dict[default] = 0

groups_dict = dict()
groups_dict[_type] = [_int]
groups_dict[optional] = True
groups_dict[default] = 1

bias_dict = dict()
bias_dict[_type] = _bool
bias_dict[optional] = True
bias_dict[default] = True

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1


transpose_params = dict()
transpose_params[in_channels] = deepcopy(in_channels_dict)
transpose_params[out_channels] = deepcopy(out_channels_dict)
transpose_params[kernel_size] = deepcopy(kernel_size_dict)
transpose_params[stride] = deepcopy(stride_dict)
transpose_params[padding] = deepcopy(padding_dict)
transpose_params[dilation] = deepcopy(dilation_dict)
transpose_params[groups] = deepcopy(groups_dict)
transpose_params[bias] = deepcopy(bias_dict)

transpose_dict = dict()
transpose_dict[path] = "torch.nn.ConvTranspose2d"
transpose_dict[params] = deepcopy(transpose_params)

layers_dict[transpose2d] = deepcopy(transpose_dict)

# Transposed 3D Convolution Layer
in_channels_dict = dict()
in_channels_dict[_type] = [_int]
in_channels_dict[optional] = False

out_channels_dict = dict()
out_channels_dict[_type] = [_int]
out_channels_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

output_padding_dict = dict()
output_padding_dict[_type] = [_int, _tuple]
output_padding_dict[optional] = True
output_padding_dict[default] = 0

groups_dict = dict()
groups_dict[_type] = [_int]
groups_dict[optional] = True
groups_dict[default] = 1

bias_dict = dict()
bias_dict[_type] = _bool
bias_dict[optional] = True
bias_dict[default] = True

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1


transpose_params = dict()
transpose_params[in_channels] = deepcopy(in_channels_dict)
transpose_params[out_channels] = deepcopy(out_channels_dict)
transpose_params[kernel_size] = deepcopy(kernel_size_dict)
transpose_params[stride] = deepcopy(stride_dict)
transpose_params[padding] = deepcopy(padding_dict)
transpose_params[dilation] = deepcopy(dilation_dict)
transpose_params[groups] = deepcopy(groups_dict)
transpose_params[bias] = deepcopy(bias_dict)

transpose_dict = dict()
transpose_dict[path] = "torch.nn.ConvTranspose3d"
transpose_dict[params] = deepcopy(transpose_params)

layers_dict[transpose3d] = deepcopy(transpose_dict)

# Unfold Layer
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

unfold_params = dict()
unfold_params[kernel_size] = kernel_size_dict
unfold_params[stride] = stride_dict
unfold_params[padding] = padding_dict
unfold_params[dilation] = dilation_dict

unfold_dict = dict()
unfold_dict[path] = "torch.nn.Unfold"
unfold_dict[params] = deepcopy(unfold_params)

layers_dict[unfold] = deepcopy(unfold_dict)

# Fold Layer
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = 1

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

fold_params = dict()
fold_params[output_size] = output_size_dict
fold_params[kernel_size] = kernel_size_dict
fold_params[stride] = stride_dict
fold_params[padding] = padding_dict
fold_params[dilation] = dilation_dict

fold_dict = dict()
fold_dict[path] = "torch.nn.Fold"
fold_dict[params] = deepcopy(fold_params)

layers_dict[fold] = deepcopy(fold_dict)

# Max Pool 1D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None 

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

maxpool1D_params = dict()
maxpool1D_params[kernel_size] = kernel_size_dict
maxpool1D_params[stride] = stride_dict
maxpool1D_params[padding] = padding_dict
maxpool1D_params[dilation] = dilation_dict
maxpool1D_params[return_indices] = return_indices_dict
maxpool1D_params[ceil_mode] = ceil_mode_dict

maxpool1D_dict = dict()
maxpool1D_dict[path] = "torch.nn.MaxPool1d"
maxpool1D_dict[params] = deepcopy(maxpool1D_params)

layers_dict[maxpool1d] = deepcopy(maxpool1D_dict)

# Max Pool 2D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None 

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

maxpool2D_params = dict()
maxpool2D_params[kernel_size] = kernel_size_dict
maxpool2D_params[stride] = stride_dict
maxpool2D_params[padding] = padding_dict
maxpool2D_params[dilation] = dilation_dict
maxpool2D_params[return_indices] = return_indices_dict
maxpool2D_params[ceil_mode] = ceil_mode_dict

maxpool2D_dict = dict()
maxpool2D_dict[path] = "torch.nn.MaxPool2d"
maxpool2D_dict[params] = deepcopy(maxpool2D_params)

layers_dict[maxpool2d] = deepcopy(maxpool2D_dict)

# Max Pool 3D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None 

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

dilation_dict = dict()
dilation_dict[_type] = [_int, _tuple]
dilation_dict[optional] = True
dilation_dict[default] = 1

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

maxpool3D_params = dict()
maxpool3D_params[kernel_size] = kernel_size_dict
maxpool3D_params[stride] = stride_dict
maxpool3D_params[padding] = padding_dict
maxpool3D_params[dilation] = dilation_dict
maxpool3D_params[return_indices] = return_indices_dict
maxpool3D_params[ceil_mode] = ceil_mode_dict

maxpool3D_dict = dict()
maxpool3D_dict[path] = "torch.nn.MaxPool3d"
maxpool3D_dict[params] = deepcopy(maxpool3D_params)

layers_dict[maxpool3d] = deepcopy(maxpool3D_dict)

# Max Unpool 1D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

maxunpool1d_params = dict()
maxunpool1d_params[kernel_size] = kernel_size_dict
maxunpool1d_params[stride] = stride_dict
maxunpool1d_params[padding] = padding_dict

maxunpool1d_dict = dict()
maxunpool1d_dict[path] = "torch.nn.MaxUnpool1d"
maxunpool1d_dict[params] = deepcopy(maxunpool1d_params)

layers_dict[maxunpool1d] = deepcopy(maxunpool1d_dict)

# Max Unpool 2D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

maxunpool2d_params = dict()
maxunpool2d_params[kernel_size] = kernel_size_dict
maxunpool2d_params[stride] = stride_dict
maxunpool2d_params[padding] = padding_dict

maxunpool2d_dict = dict()
maxunpool2d_dict[path] = "torch.nn.MaxUnpool2d"
maxunpool2d_dict[params] = deepcopy(maxunpool2d_params)

layers_dict[maxunpool2d] = deepcopy(maxunpool2d_dict)

# Max Unpool 3D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

maxunpool3d_params = dict()
maxunpool3d_params[kernel_size] = kernel_size_dict
maxunpool3d_params[stride] = stride_dict
maxunpool3d_params[padding] = padding_dict

maxunpool3d_dict = dict()
maxunpool3d_dict[path] = "torch.nn.MaxUnpool3d"
maxunpool3d_dict[params] = deepcopy(maxunpool3d_params)

layers_dict[maxunpool3d] = deepcopy(maxunpool3d_dict)

# Average pool 1D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

count_include_dict = dict()
count_include_dict[_type] = _bool
count_include_dict[optional] = True
count_include_dict[default] = True

avgpool1d_params = dict()
avgpool1d_params[kernel_size] = kernel_size_dict
avgpool1d_params[stride] = stride_dict
avgpool1d_params[padding] = padding_dict
avgpool1d_params[ceil_mode] = ceil_mode_dict
avgpool1d_params[count_include] = count_include_dict

avgpool1d_dict = dict()
avgpool1d_dict[path] = "torch.nn.AvgPool1d"
avgpool1d_dict[params] = deepcopy(avgpool1d_dict)

layers_dict[avgpool1d] = deepcopy(avgpool1d_dict)

# Average pool 2D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

count_include_dict = dict()
count_include_dict[_type] = _bool
count_include_dict[optional] = True
count_include_dict[default] = True

avgpool2d_params = dict()
avgpool2d_params[kernel_size] = kernel_size_dict
avgpool2d_params[stride] = stride_dict
avgpool2d_params[padding] = padding_dict
avgpool1d_params[ceil_mode] = ceil_mode_dict
avgpool1d_params[count_include] = count_include_dict

avgpool2d_dict = dict()
avgpool2d_dict[path] = "torch.nn.AvgPool2d"
avgpool2d_dict[params] = deepcopy(avgpool2d_params)

layers_dict[avgpool2d] = deepcopy(avgpool2d_dict)

# Average pool 3D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = True
padding_dict[default] = 0

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

count_include_dict = dict()
count_include_dict[_type] = _bool
count_include_dict[optional] = True
count_include_dict[default] = True

avgpool3d_params = dict()
avgpool3d_params[kernel_size] = kernel_size_dict
avgpool3d_params[stride] = stride_dict
avgpool3d_params[padding] = padding_dict
avgpool3d_params[ceil_mode] = ceil_mode_dict
avgpool3d_params[count_include] = count_include_dict

avgpool3d_dict = dict()
avgpool3d_dict[path] = "torch.nn.AvgPool3d"
avgpool3d_dict[params] = deepcopy(avgpool3d_params)

layers_dict[avgpool2d] = deepcopy(avgpool3d_dict)

# Fractional Max Pool 2D
kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = True
output_size_dict[default] = None

output_ratio_dict = dict()
output_ratio_dict[_type] = [_float]
output_ratio_dict[optional] = None

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

fractionalmaxpool2d_params = dict()
fractionalmaxpool2d_params[kernel_size] = kernel_size_dict
fractionalmaxpool2d_params[output_size] = output_size_dict
fractionalmaxpool2d_params[output_ratio] = output_ratio_dict
fractionalmaxpool2d_params[return_indices] = return_indices_dict

fractionalmaxpool2d_dict = dict()
fractionalmaxpool2d_dict[path] = "torch.nn.FractionalMaxPool2d"
fractionalmaxpool2d_dict[params] = deepcopy(fractionalmaxpool2d_params)

layers_dict[fractionalmaxpool2d] = deepcopy(fractionalmaxpool2d_dict)

# LP Pool 1D
norm_type_dict = dict()
norm_type_dict[_type] = [_int]
norm_type_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

lppool1d_params = dict()
lppool1d_params[norm_type] = norm_type_dict
lppool1d_params[kernel_size] = kernel_size_dict
lppool1d_params[stride] = stride_dict
lppool1d_params[ceil_mode] = ceil_mode_dict

lppool1d_dict = dict()
lppool1d_dict[path] = "torch.nn.LPPool1d"
lppool1d_dict[params] = deepcopy(lppool1d_params)

layers_dict[lppool1d] = deepcopy(lppool1d_dict)



# LP Pool 2D
norm_type_dict = dict()
norm_type_dict[_type] = [_int]
norm_type_dict[optional] = False

kernel_size_dict = dict()
kernel_size_dict[_type] = [_int, _tuple]
kernel_size_dict[optional] = False

stride_dict = dict()
stride_dict[_type] = [_int, _tuple]
stride_dict[optional] = True
stride_dict[default] = None

ceil_mode_dict = dict()
ceil_mode_dict[_type] = [_bool]
ceil_mode_dict[optional] = True
ceil_mode_dict[default] = False

lppool2d_params = dict()
lppool2d_params[norm_type] = norm_type_dict
lppool2d_params[kernel_size] = kernel_size_dict
lppool2d_params[stride] = stride_dict
lppool2d_params[ceil_mode] = ceil_mode_dict

lppool2d_dict = dict()
lppool2d_dict[path] = "torch.nn.LPPool2d"
lppool2d_dict[params] = deepcopy(lppool2d_params)

layers_dict[lppool2d] = deepcopy(lppool2d_dict)

# Adaptive Max Pooling 1D
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

adaptivemaxpool1d_params = dict()
adaptivemaxpool1d_params[output_size] = output_size_dict
adaptivemaxpool1d_params[return_indices] = return_indices_dict

adaptivemaxpool1d_dict = dict()
adaptivemaxpool1d_dict[path] = "torch.nn.AdaptiveMaxPool1d"
adaptivemaxpool1d_dict[params] = deepcopy(adaptivemaxpool1d_params)

layers_dict[adaptivemaxpool1d] = deepcopy(adaptivemaxpool1d_dict)

# Adaptive Max Pooling 2D
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

adaptivemaxpool2d_params = dict()
adaptivemaxpool2d_params[output_size] = output_size_dict
adaptivemaxpool2d_params[return_indices] = return_indices_dict

adaptivemaxpool2d_dict = dict()
adaptivemaxpool2d_dict[path] = "torch.nn.AdaptiveMaxPool2d"
adaptivemaxpool2d_dict[params] = deepcopy(adaptivemaxpool2d_params)

layers_dict[adaptivemaxpool1d] = deepcopy(adaptivemaxpool2d_dict)

# Adaptive Max Pooling 3D
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

return_indices_dict = dict()
return_indices_dict[_type] = [_bool]
return_indices_dict[optional] = True
return_indices_dict[default] = False

adaptivemaxpool3d_params = dict()
adaptivemaxpool3d_params[output_size] = output_size_dict
adaptivemaxpool3d_params[return_indices] = return_indices_dict

adaptivemaxpool3d_dict = dict()
adaptivemaxpool3d_dict[path] = "torch.nn.AdaptiveMaxPoo31d"
adaptivemaxpool3d_dict[params] = deepcopy(adaptivemaxpool3d_params)

layers_dict[adaptivemaxpool1d] = deepcopy(adaptivemaxpool3d_dict)

# Adaptive Average Pooling 1D
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

adaptiveavgpool1d_params = dict()
adaptiveavgpool1d_params[output_size] = output_size_dict

adaptiveavgpool1d_dict = dict()
adaptiveavgpool1d_dict[path] = "torch.nn.AdaptiveAvgPool1d"
adaptiveavgpool1d_dict[params] = deepcopy(adaptiveavgpool1d_params)

layers_dict[adaptiveavgpool1d] = deepcopy(adaptiveavgpool1d_dict)

# Adaptive Average Pooling 2D
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

adaptiveavgpool2d_params = dict()
adaptiveavgpool2d_params[output_size] = output_size_dict

adaptiveavgpool2d_dict = dict()
adaptiveavgpool2d_dict[path] = "torch.nn.AdaptiveAvgPool2d"
adaptiveavgpool2d_dict[params] = deepcopy(adaptiveavgpool2d_params)

layers_dict[adaptiveavgpool2d] = deepcopy(adaptiveavgpool2d_dict)

# Adaptive Average Pooling 3D
output_size_dict = dict()
output_size_dict[_type] = [_int, _tuple]
output_size_dict[optional] = False

adaptiveavgpool3d_params = dict()
adaptiveavgpool3d_params[output_size] = output_size_dict

adaptiveavgpool3d_dict = dict()
adaptiveavgpool3d_dict[path] = "torch.nn.AdaptiveAvgPool3d"
adaptiveavgpool3d_dict[params] = deepcopy(adaptiveavgpool3d_params)

layers_dict[adaptiveavgpool3d] = deepcopy(adaptiveavgpool3d_dict)

# Reflection Padding 1D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

reflectionpad1d_params = dict()
reflectionpad1d_params[padding] = padding_dict

reflectionpad1d_dict = dict()
reflectionpad1d_dict[path] = "torch.nn.ReflectionPad1d"
reflectionpad1d_dict[params] = deepcopy(reflectionpad1d_params)

layers_dict[reflectionpad1d] = deepcopy(reflectionpad1d_dict)

# Reflection Padding 2D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

reflectionpad2d_params = dict()
reflectionpad2d_params[padding] = padding_dict

reflectionpad2d_dict = dict()
reflectionpad2d_dict[path] = "torch.nn.ReflectionPad2d"
reflectionpad2d_dict[params] = deepcopy(reflectionpad2d_params)

layers_dict[reflectionpad2d] = deepcopy(reflectionpad2d_dict)

# Replication Padding 1D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

replicationpad1d_params = dict()
replicationpad1d_params[padding] = padding_dict

replicationpad1d_dict = dict()
replicationpad1d_dict[path] = "torch.nn.ReplicationPad1d"
replicationpad1d_dict[params] = deepcopy(replicationpad1d_params)

layers_dict[replicationpad1d] = deepcopy(replicationpad1d_dict)

# Replication Padding 2D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

replicationpad2d_params = dict()
replicationpad2d_params[padding] = padding_dict

replicationpad2d_dict = dict()
replicationpad2d_dict[path] = "torch.nn.ReplicationPad2d"
replicationpad2d_dict[params] = deepcopy(replicationpad2d_params)

layers_dict[replicationpad2d] = deepcopy(replicationpad2d_dict)

# Replication Padding 3D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

replicationpad3d_params = dict()
replicationpad3d_params[padding] = padding_dict

replicationpad3d_dict = dict()
replicationpad3d_dict[path] = "torch.nn.ReplicationPad3d"
replicationpad3d_dict[params] = deepcopy(replicationpad3d_params)

layers_dict[replicationpad3d] = deepcopy(replicationpad3d_dict)

# Zero Padding 2D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

zeropad2d_params = dict()
zeropad2d_params[padding] = padding_dict

zeropad2d_dict = dict()
zeropad2d_dict[path] = "torch.nn.ZeroPad2d"
zeropad2d_dict[params] = deepcopy(zeropad2d_params)

layers_dict[zeropad2d] = deepcopy(zeropad2d_dict)

# Constant Padding 1D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

value_dict = dict()
value_dict[_type] = [_int, _tuple]
value_dict[optional] = False

constantpad1d_params = dict()
constantpad1d_params[padding] = padding_dict
constantpad1d_params[value] = value_dict

constantpad1d_dict = dict()
constantpad1d_dict[path] = "torch.nn.ConstantPad1d"
constantpad1d_dict[params] = deepcopy(constantpad1d_params)

layers_dict[constantpad1d] = deepcopy(constantpad1d_dict)

# Constant Padding 2D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

value_dict = dict()
value_dict[_type] = [_int, _tuple]
value_dict[optional] = False

constantpad2d_params = dict()
constantpad2d_params[padding] = padding_dict
constantpad2d_params[value] = value_dict

constantpad2d_dict = dict()
constantpad2d_dict[path] = "torch.nn.ConstantPad2d"
constantpad2d_dict[params] = deepcopy(constantpad2d_params)

layers_dict[constantpad2d] = deepcopy(constantpad2d_dict)

# Constant Padding 3D
padding_dict = dict()
padding_dict[_type] = [_int, _tuple]
padding_dict[optional] = False

value_dict = dict()
value_dict[_type] = [_int, _tuple]
value_dict[optional] = False

constantpad3d_params = dict()
constantpad3d_params[padding] = padding_dict
constantpad3d_params[value] = value_dict

constantpad3d_dict = dict()
constantpad3d_dict[path] = "torch.nn.ConstantPad3d"
constantpad3d_dict[params] = deepcopy(constantpad3d_params)

layers_dict[constantpad3d] = deepcopy(constantpad3d_dict)

# ELU
alpha_dict = dict()
alpha_dict[_type] = [_float]
alpha_dict[optional] = True
alpha_dict[default] = 1

inplace_dict = dict()
inplace_dict[_type] = _bool
inplace_dict[optional] = True
inplace_dict[default] = False

elu_params = dict()
elu_params[alpha] = alpha_dict
elu_params[inplace] = inplace_dict

elu_dict = dict()
elu_dict[path] = "torch.nn.ELU"
elu_dict[params] = deepcopy(elu_params)

layers_dict[elu] = deepcopy(elu_dict)

# Hardshrink
lambd_dict = dict()
lambd_dict[_type] = [_float]
lambd_dict[optional] = True
lambd_dict[default] = 0.5

hardshrink_params = dict()
hardshrink_params[lambd] = lambd_dict

hardshrink_dict = dict()
hardshrink_dict[path] = "torch.nn.ELU"
hardshrink_dict[params] = deepcopy(hardshrink_params)

layers_dict[hardshrink] = deepcopy(hardshrink_dict)

# Hardtanh
min_val_dict = dict()
min_val_dict[_type] = _float
min_val_dict[optional] = True
min_val_dict[default] = -1

max_val_dict = dict()
max_val_dict[_type] = _float
max_val_dict[optional] = True
max_val_dict[default] = 1

inplace_dict = dict()
inplace_dict[_type] = _bool
inplace_dict[optional] = True
inplace_dict[default] = False

min_value_dict = dict()
min_value_dict[_type] = _float
min_value_dict[optional] = True
min_value_dict[default] = None

max_value_dict = dict()
max_value_dict[_type] = _float
max_value_dict[optional] = False
max_value_dict[default] = None

hardtanh_params = dict()
hardtanh_params[min_val] = min_val_dict
hardtanh_params[max_val] = max_val_dict
hardtanh_params[inplace] = inplace_dict
hardtanh_params[min_value] = min_value_dict
hardtanh_params[max_value] = max_value_dict

hardtanh_dict = dict()
hardtanh_dict[path] = "torch.nn.Hardtanh"
hardtanh_dict[params] = deepcopy(hardtanh_params)

layers_dict[hardtanh] = hardtanh_dict


# Print the current working directory and write the dictionary to JSON file
import os
cwd = os.getcwd()
print(cwd)
with open('torch_params.json', 'w') as fp:
    json.dump(layers_dict, fp)

print(layers_dict)














