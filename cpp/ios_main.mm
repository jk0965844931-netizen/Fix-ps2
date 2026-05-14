#import <UIKit/UIKit.h>

#include "PerformanceDefaults.h"

@interface IPSX2AppDelegate : UIResponder <UIApplicationDelegate>
@property(nonatomic, strong) UIWindow *window;
@end

@interface IPSX2ViewController : UIViewController
@end

@implementation IPSX2ViewController

- (void)viewDidLoad {
  [super viewDidLoad];
  self.view.backgroundColor = [UIColor colorWithRed:0.06 green:0.08 blue:0.12 alpha:1.0];

  UILabel *title = [[UILabel alloc] initWithFrame:CGRectZero];
  title.translatesAutoresizingMaskIntoConstraints = NO;
  title.text = @"iPSX2";
  title.textColor = UIColor.whiteColor;
  title.font = [UIFont boldSystemFontOfSize:36.0];
  title.textAlignment = NSTextAlignmentCenter;

  UILabel *subtitle = [[UILabel alloc] initWithFrame:CGRectZero];
  subtitle.translatesAutoresizingMaskIntoConstraints = NO;
  subtitle.numberOfLines = 0;
  subtitle.textColor = [UIColor colorWithWhite:0.82 alpha:1.0];
  subtitle.font = [UIFont systemFontOfSize:16.0 weight:UIFontWeightRegular];
  subtitle.textAlignment = NSTextAlignmentCenter;
  subtitle.text = [NSString stringWithFormat:
      @"Unsigned build shell ready. Apply the smooth preset to a real PCSX2/iPSX2 config for Metal rendering, native resolution, MTVU, and safe frame pacing.\n\n%lu performance defaults compiled in.",
      static_cast<unsigned long>(kIPSX2SmoothDefaults.size())];

  UIStackView *stack = [[UIStackView alloc] initWithArrangedSubviews:@[ title, subtitle ]];
  stack.translatesAutoresizingMaskIntoConstraints = NO;
  stack.axis = UILayoutConstraintAxisVertical;
  stack.alignment = UIStackViewAlignmentCenter;
  stack.spacing = 18.0;

  [self.view addSubview:stack];
  [NSLayoutConstraint activateConstraints:@[
    [stack.leadingAnchor constraintGreaterThanOrEqualToAnchor:self.view.safeAreaLayoutGuide.leadingAnchor constant:24.0],
    [stack.trailingAnchor constraintLessThanOrEqualToAnchor:self.view.safeAreaLayoutGuide.trailingAnchor constant:-24.0],
    [stack.centerXAnchor constraintEqualToAnchor:self.view.centerXAnchor],
    [stack.centerYAnchor constraintEqualToAnchor:self.view.centerYAnchor],
    [subtitle.widthAnchor constraintLessThanOrEqualToConstant:620.0]
  ]];
}

@end

@implementation IPSX2AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  (void)application;
  (void)launchOptions;
  self.window = [[UIWindow alloc] initWithFrame:UIScreen.mainScreen.bounds];
  self.window.rootViewController = [[IPSX2ViewController alloc] init];
  [self.window makeKeyAndVisible];
  return YES;
}

@end

int main(int argc, char *argv[]) {
  @autoreleasepool {
    return UIApplicationMain(argc, argv, nil, NSStringFromClass(IPSX2AppDelegate.class));
  }
}
