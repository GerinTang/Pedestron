import torch.nn as nn


norm_cfg = {'BN': nn.BatchNorm2d, 'SyncBN': None, 'GN': nn.GroupNorm}


def build_norm_layer(cfg, num_features):
    """
    cfg should contain:
        type (str): identify norm layer type.
        layer args: args needed to instantiate a norm layer.
        frozen (bool): [optional] whether stop gradient updates
            of norm layer, it is helpful to set frozen mode
            in backbone's norms.
    """
    assert isinstance(cfg, dict) and 'type' in cfg
    cfg_ = cfg.copy()
    layer_type = cfg_.pop('type')
    frozen = cfg_.pop('frozen') if 'frozen' in cfg_ else False

    # args name matching
    if layer_type == 'GN':
        assert 'num_groups' in cfg
        cfg_.setdefault('num_channels', num_features)
    elif layer_type == 'BN':
        cfg_.setdefault('num_features', num_features)
    cfg_.setdefault('eps', 1e-5)

    if layer_type not in norm_cfg:
        raise KeyError('Unrecognized norm type {}'.format(layer_type))
    elif norm_cfg[layer_type] is None:
        raise NotImplementedError

    norm = norm_cfg[layer_type](**cfg_)
    if frozen:
        for param in norm.parameters():
            param.requires_grad = False
    return norm
