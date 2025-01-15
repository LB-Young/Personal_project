from load_local_api_keys import load_local_api_keys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown2

async def dict_to_multiline_string(d, indent=0):
    result = ""
    for key, value in d.items():
        if isinstance(value, dict):  # 如果值是字典，递归处理
            inner = await dict_to_multiline_string(value, indent + 4)
            result += " " * indent + f"{key}:\n" + inner
        else:  # 否则直接添加键值对
            result += " " * indent + f"{key}: {value}\n"
    return result

class SendEmail:
    name = "send_email" 
    description = "将内容通过邮件发送给指定的邮箱。"
    inputs = {
        "content": {
            "type": "string",
            "description": "邮件内容"
            },
        "subject": {
            "type": "string",
            "description": "邮件主题"
            },
        "to": {
            "type": "string",
            "description": "邮件发送给谁"
            }
    }
    outputs = {
        "content": {
            "type": "string",
            "description": "邮件发送是否成功的提醒"
            }
    }
    props = {}

    async def run(content="", subject="", to="", params_format=False):
        if params_format:
            return ['content', 'subject', 'to']
        # Set up the SMTP server
        smtp_server = "smtp.qq.com"
        smtp_port = 465  # 修改为SSL端口465
        smtp_username = "823707202@qq.com"
        # 需要使用应用专用密码而不是普通密码
        # 请在Google账户设置中生成应用专用密码: https://myaccount.google.com/security
        smtp_password = load_local_api_keys("qq_mail_shouquanma") # 替换为应用专用密码
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = ""
        msg['Subject'] = subject
        if isinstance(content, dict):
            content = await dict_to_multiline_string(content, 0)
        elif isinstance(content, list):
            content = "[" + "\n".join(content) + "\n]" 
        else:
            content = str(content)

        # 创建纯文本版本（作为后备）
        text_part = MIMEText(content, 'plain', 'utf-8')
        
        # 转换 Markdown 为 HTML 并创建 HTML 版本
        html_content = markdown2.markdown(content, extras=['tables', 'code-friendly', 'fenced-code-blocks'])
    
    # 添加一些基本的 CSS 样式
        styled_html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
                    pre {{ background: #f4f4f4; padding: 1em; border-radius: 4px; overflow-x: auto; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; }}
                    th {{ background-color: #f4f4f4; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """
        html_part = MIMEText(styled_html, 'html', 'utf-8')

        msg.attach(html_part)


        # msg.attach(MIMEText(content, 'html', 'utf-8'))
        try:
            # 连接 SMTP 服务器
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用 SSL 加密
            server.login(smtp_username, smtp_password)  # 登录邮箱
            server.sendmail(from_addr=smtp_username, to_addrs="lby15356@gmail.com", msg=msg.as_string())  # 发送邮件
            print("邮件发送成功！")
            return f"Send email to {to} successfully"
        except smtplib.SMTPException as e:
            print(f"邮件发送失败：{e}")
            return "failed"
        finally:
            server.quit()

if __name__ == '__main__':
    import asyncio
    content = """
    # AutoTrust: Benchmarking Trustworthiness in Large Vision Language Models for Autonomous Driving
https://arxiv.org/abs/2412.15206
### 基本信息
作者: Shuo Xing, Hongyuan Hua, Xiangbo Gao, Shenzhe Zhu, Renjie Li, Kexin Tian, Xiaopeng Li, Heng Huang, Tianbao Yang, Zhangyang Wang, Yang Zhou, Huaxiu Yao, Zhengzhong Tu
研究团队: Texas A&M University, University of Toronto, University of Michigan, University of Wisconsin-Madison, University of Maryland, University of Texas at Austin, University of North Carolina at Chapel Hill
### 论文解读
#### 摘要
近年来，针对自动驾驶（AD）的大型视觉语言模型（VLMs）在场景理解和推理方面表现出色，使其成为端到端驾驶系统的候选者。然而，关于DriveVLMs的信任度研究有限，这直接影响了公共交通安全。本文介绍了AutoTrust，一个用于评估自动驾驶中大型视觉语言模型信任度的综合基准，涵
盖了信任度、安全性、鲁棒性、隐私和公平性等多个方面。我们构建了最大的视觉问答数据集，用于研究驾驶场景中的信任问题，包含超过10k个 
独特场景和18k个查询。我们评估了六个公开可用的VLMs，从通用模型到专业模型，从开源模型到商业模型。我们的全面评估揭示了DriveVLMs在信
任度威胁方面的先前未发现的漏洞。具体来说，我们发现通用VLMs如LLaVA-v1.6和GPT-4o-mini在整体信任度上出人意料地优于专门为驾驶优化的 
模型。DriveVLMs如DriveLM-Agent特别容易泄露敏感信息。此外，通用和专业VLMs都容易受到对抗性攻击，并且在确保多样环境和人群的无偏决策
方面表现不佳。我们的研究呼吁立即采取决定性行动来解决DriveVLMs的信任度问题，这对公共安全和依赖自动驾驶交通系统的所有公民的福祉至 
关重要。我们的基准可在https://github.com/taco-group/AutoTrust 获取，排行榜可在https://taco-group.github.io/AutoTrust/ 查看。    
#### 研究的问题
本文研究的核心问题是：如何评估和提升自动驾驶中大型视觉语言模型的信任度，特别是在信任度、安全性、鲁棒性、隐私和公平性等方面。    
#### 核心思路
本文的核心思路是引入AutoTrust基准，通过构建大规模的视觉问答数据集，评估六个公开可用的VLMs在不同信任度维度上的表现。研究团队通过 
实验揭示了现有DriveVLMs在信任度方面的漏洞，并提出了改进建议。
#### 实验的结果
实验结果表明：
1. 通用VLMs在信任度上表现优于专门为驾驶优化的模型。
2. DriveVLMs在隐私保护方面表现不佳，容易泄露敏感信息。
3. 通用和专业VLMs都容易受到对抗性攻击，并且在确保无偏决策方面表现不佳。
4. 研究呼吁立即采取行动解决DriveVLMs的信任度问题，以确保公共安全和自动驾驶系统的可靠性。
# 提取的论文标题
Human-Humanoid Robots Cross-Embodiment Behavior-Skill Transfer Using Decomposed Adversarial Learning from Demonstration

提取的论文链接
https://arxiv.org/abs/2412.15166

### 基本信息
提取的作者、研究团队
- 作者: Junjia Liu, Zhuo Li, Minghao Yu, Zhipeng Dong, Sylvain Calinon, Darwin Caldwell, Fei Chen
- 研究团队:
  - Department of Mechanical and Automation Engineering, T-Stone Robotics Institute, The Chinese University of Hong Kong        
  - Idiap Research Institute, Martigny, Switzerland
  - Department of Advanced Robotics, Istituto Italiano di Tecnologia, Genoa, Italy

### 论文解读
#### 摘要
Humanoid robots are envisioned as embodied intelligent agents capable of performing a wide range of human-level loco-manipulation tasks, particularly in scenarios requiring strenuous and repetitive labor. However, learning these skills is challenging due to the high degrees of freedom of humanoid robots, and collecting sufficient training data for humanoid is a laborious process. Given the rapid introduction of new humanoid platforms, a cross-embodiment framework that allows generalizable skill transfer is 
becoming increasingly critical. To address this, we propose a transferable framework that reduces the data bottleneck by using a unified digital human model as a common prototype and bypassing the need for re-training on every new robot platform. The model learns behavior primitives from human demonstrations through adversarial imitation, and the complex robot structures are decomposed into functional components, each trained independently and dynamically coordinated. Task generalization is achieved through a human-object interaction graph, and skills are transferred to different robots via embodiment-specific kinematic motion retargeting and dynamic fine-tuning. Our framework is validated on five humanoid robots with diverse configurations, demonstrating stable loco-manipulation and highlighting its effectiveness in reducing data requirements and increasing the efficiency of skill transfer across platforms.

#### 研究的问题
- 人形机器人学习复杂任务（如行走和操作）的挑战，特别是由于其高自由度和数据收集的困难。
- 不同人形机器人平台之间的技能转移问题，尤其是由于配置差异导致的技能转移效率低下。

#### 核心思路
- 提出一个跨体现的框架，使用统一的数字人类模型作为通用原型，减少数据瓶颈。
- 通过对抗性模仿学习从人类演示中学习行为原语。
- 将复杂的机器人结构分解为功能组件，每个组件独立训练并通过动态协调进行整合。
- 通过人类-物体交互图实现任务泛化，并通过体现特定的运动重定向和动态微调将技能转移到不同机器人。

#### 实验的结果
- 在五种不同配置的人形机器人上验证了该框架，展示了稳定的行走和操作能力。
- 实验结果表明，该框架有效减少了数据需求，并提高了跨平台技能转移的效率。
- 与现有方法相比，该框架在任务完成率和训练时间上均有显著提升。
# AutoTrust: Benchmarking Trustworthiness in Large Vision Language Models for Autonomous Driving
https://arxiv.org/abs/2412.15206
### 基本信息
作者: Shuo Xing, Hongyuan Hua, Xiangbo Gao, Shenzhe Zhu, Renjie Li, Kexin Tian, Xiaopeng Li, Heng Huang, Tianbao Yang, Zhangyang Wang, Yang Zhou, Huaxiu Yao, Zhengzhong Tu
研究团队: Texas A&M University, University of Toronto, University of Michigan, University of Wisconsin-Madison, University of Maryland, University of Texas at Austin, University of North Carolina at Chapel Hill
### 论文解读
#### 摘要
近年来，针对自动驾驶（AD）的大型视觉语言模型（VLMs）在场景理解和推理方面表现出色，使其成为端到端驾驶系统的候选者。然而，关于DriveVLMs的信任度研究有限，这直接影响了公共交通安全。本文介绍了AutoTrust，一个用于评估自动驾驶中大型视觉语言模型信任度的综合基准，涵
盖了信任度、安全性、鲁棒性、隐私和公平性等多个方面。我们构建了最大的视觉问答数据集，用于研究驾驶场景中的信任问题，包含超过10k个 
独特场景和18k个查询。我们评估了六个公开可用的VLMs，从通用模型到专业模型，从开源模型到商业模型。我们的全面评估揭示了DriveVLMs在信
任度威胁方面的先前未发现的漏洞。具体来说，我们发现通用VLMs如LLaVA-v1.6和GPT-4o-mini在整体信任度上出人意料地优于专门为驾驶优化的 
模型。DriveVLMs如DriveLM-Agent特别容易泄露敏感信息。此外，通用和专业VLMs都容易受到对抗性攻击，并且在确保多样环境和人群的无偏决策
方面表现不佳。我们的研究呼吁立即采取决定性行动来解决DriveVLMs的信任度问题，这对公共安全和依赖自动驾驶交通系统的所有公民的福祉至 
关重要。我们的基准可在https://github.com/taco-group/AutoTrust 获取，排行榜可在https://taco-group.github.io/AutoTrust/ 查看。    
#### 研究的问题
本文研究的核心问题是：如何评估和提升自动驾驶中大型视觉语言模型的信任度，特别是在信任度、安全性、鲁棒性、隐私和公平性等方面。    
#### 核心思路
本文的核心思路是引入AutoTrust基准，通过构建大规模的视觉问答数据集，评估六个公开可用的VLMs在不同信任度维度上的表现。研究团队通过 
实验揭示了现有DriveVLMs在信任度方面的漏洞，并提出了改进建议。
#### 实验的结果
实验结果表明：
1. 通用VLMs在信任度上表现优于专门为驾驶优化的模型。
2. DriveVLMs在隐私保护方面表现不佳，容易泄露敏感信息。
3. 通用和专业VLMs都容易受到对抗性攻击，并且在确保无偏决策方面表现不佳。
4. 研究呼吁立即采取行动解决DriveVLMs的信任度问题，以确保公共安全和自动驾驶系统的可靠性。
# 提取的论文标题
Human-Humanoid Robots Cross-Embodiment Behavior-Skill Transfer Using Decomposed Adversarial Learning from Demonstration

提取的论文链接
https://arxiv.org/abs/2412.15166

### 基本信息
提取的作者、研究团队
- 作者: Junjia Liu, Zhuo Li, Minghao Yu, Zhipeng Dong, Sylvain Calinon, Darwin Caldwell, Fei Chen
- 研究团队:
  - Department of Mechanical and Automation Engineering, T-Stone Robotics Institute, The Chinese University of Hong Kong        
  - Idiap Research Institute, Martigny, Switzerland
  - Department of Advanced Robotics, Istituto Italiano di Tecnologia, Genoa, Italy

### 论文解读
#### 摘要
Humanoid robots are envisioned as embodied intelligent agents capable of performing a wide range of human-level loco-manipulation tasks, particularly in scenarios requiring strenuous and repetitive labor. However, learning these skills is challenging due to the high degrees of freedom of humanoid robots, and collecting sufficient training data for humanoid is a laborious process. Given the rapid introduction of new humanoid platforms, a cross-embodiment framework that allows generalizable skill transfer is 
becoming increasingly critical. To address this, we propose a transferable framework that reduces the data bottleneck by using a unified digital human model as a common prototype and bypassing the need for re-training on every new robot platform. The model learns behavior primitives from human demonstrations through adversarial imitation, and the complex robot structures are decomposed into functional components, each trained independently and dynamically coordinated. Task generalization is achieved through a human-object interaction graph, and skills are transferred to different robots via embodiment-specific kinematic motion retargeting and dynamic fine-tuning. Our framework is validated on five humanoid robots with diverse configurations, demonstrating stable loco-manipulation and highlighting its effectiveness in reducing data requirements and increasing the efficiency of skill transfer across platforms.

#### 研究的问题
- 不同人形机器人平台之间的技能转移问题，尤其是由于配置差异导致的技能转移效率低下。

#### 核心思路
- 通过对抗性模仿学习从人类演示中学习行为原语。
- 将复杂的机器人结构分解为功能组件，每个组件独立训练并通过动态协调进行整合。
- 通过人类-物体交互图实现任务泛化，并通过体现特定的运动重定向和动态微调将技能转移到不同机器人。

#### 实验的结果
- 在五种不同配置的人形机器人上验证了该框架，展示了稳定的行走和操作能力。
- 实验结果表明，该框架有效减少了数据需求，并提高了跨平台技能转移的效率。
- 与现有方法相比，该框架在任务完成率和训练时间上均有显著提升。
"""
    res = asyncio.run(send_email(content, "1", to="lby15356@gmail.com"))
    print(res)
