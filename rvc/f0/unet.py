import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        return self.conv(x)


class Encoder(nn.Module):
    def __init__(self, in_channels=1):
        super().__init__()
        self.bn = nn.BatchNorm2d(in_channels)
        
        # Encoder layers
        self.layers = nn.ModuleList([
            ConvBlock(in_channels, 32),
            ConvBlock(32, 64),
            ConvBlock(64, 128),
            ConvBlock(128, 256),
            ConvBlock(256, 512)
        ])
        
        self.pool = nn.MaxPool2d(2)
    
    def forward(self, x):
        x = self.bn(x)
        features = []
        
        for layer in self.layers:
            x = layer(x)
            features.append(x)
            x = self.pool(x)
        
        return x, features


class Decoder(nn.Module):
    def __init__(self, out_channels=1):
        super().__init__()
        
        # Decoder layers
        self.upconv5 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.conv5 = ConvBlock(512, 256)
        
        self.upconv4 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv4 = ConvBlock(256, 128)
        
        self.upconv3 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv3 = ConvBlock(128, 64)
        
        self.upconv2 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.conv2 = ConvBlock(64, 32)
        
        self.final_conv = nn.Conv2d(32, out_channels, 1)
    
    def forward(self, x, features):
        # Reverse the features list for decoder
        features = features[::-1]
        
        x = self.upconv5(x)
        x = torch.cat([x, features[1]], dim=1)
        x = self.conv5(x)
        
        x = self.upconv4(x)
        x = torch.cat([x, features[2]], dim=1)
        x = self.conv4(x)
        
        x = self.upconv3(x)
        x = torch.cat([x, features[3]], dim=1)
        x = self.conv3(x)
        
        x = self.upconv2(x)
        x = torch.cat([x, features[4]], dim=1)
        x = self.conv2(x)
        
        x = self.final_conv(x)
        return x


class UNet(nn.Module):
    def __init__(self, in_channels=1, out_channels=1):
        super().__init__()
        self.encoder = Encoder(in_channels)
        self.decoder = Decoder(out_channels)
    
    def forward(self, x):
        encoded, features = self.encoder(x)
        decoded = self.decoder(encoded, features)
        return decoded
