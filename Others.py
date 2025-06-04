from torch import nn


class CasualConvld(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size, dilation, A=False, **kwargs):
        super(CasualConvld, self).__init__()

        """The general idea is the following: We take the built-in PyTorch Convld. Then, we must 
 pick a proper padding, becausewe must ensure the convolutional is casual. Eventually, we
 must remove some final elements of theoutput, because we simply don't need them!Since 
 CasualConvld is still a convolution, we must definethe kernel size, dilation and whether 
 it is option A (A=True) or option b (A=False). Rememberthatby playing with dilation we 
 can enlarge the size of the memory."""
        #attributes
        self.kernel_size = kernel_size
        self.dilation = dilation
        self.A = A # whether option A (A=True) or b (A=False)
        self.padding = (kernel_size - 1) * dilation + A * 1

        # we will do padding by ourselves in the forwaerd pass!
        self.convld = nn.Convld(in_channels, out_channels, kernel_size, stride=1,
                                padding=0, dilation=dilation, **kwargs)
        
    def forward(self, x):
        #we do padding only from the left. This os more dfficient implementation.
        x = nn.functional.pad(x, (self.padding, 0))
        convld_out = self.convld(x)
        if self.A:
            """Remember that we cannot be dependent on the current component; therefore, the 
            last component is removed"""
            return convld_out[:, :, : -1]
        else:
            return convld_out
